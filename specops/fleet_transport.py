#!/usr/bin/env python3
"""Standalone, read-only Fleet MCP client for a caller-provisioned fleet.read grant.
No token discovery, OAuth consent automation, execution or release authorization.
Tokens are never printed or persisted. HTTPS JSON transport only; fail closed.
"""
import json
import re
import ssl
import urllib.parse
import urllib.request
import urllib.error
import unittest

TOOLS = frozenset({"fleet_jobs_status", "fleet_command_status"})
JOB = re.compile(r"[0-9a-f]{32}")
MAX_BODY = 2_000_000

class TransportError(RuntimeError):
    pass

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def unique_object(pairs):
    obj = {}
    for k, v in pairs:
        if k in obj:
            raise TransportError("duplicate JSON field")
        obj[k] = v
    return obj

class FleetReadClient:
    def __init__(self, endpoint, token, opener=None):
        u = urllib.parse.urlsplit(endpoint)
        if (u.scheme != "https" or not u.hostname or u.username or u.password
                or u.query or u.fragment or u.path != "/mcp"):
            raise ValueError("expected explicit HTTPS /mcp endpoint")
        if not isinstance(token, str) or not token or any(ord(c) < 33 or ord(c) > 126 for c in token):
            raise ValueError("missing or invalid scoped token")
        self.endpoint = endpoint
        self._token = token
        self._opener = opener or urllib.request.build_opener(
            urllib.request.ProxyHandler({}), NoRedirect(),
            urllib.request.HTTPSHandler(context=ssl.create_default_context()))
        self._seq = 0
        self._session = None
        self._protocol = None

    def _request(self, method, params, notification=False):
        self._seq += 1
        obj = {"jsonrpc":"2.0","method":method,"params":params}
        if not notification:
            obj["id"] = self._seq
        headers = {"Authorization":"Bearer "+self._token,
                   "Content-Type":"application/json",
                   "Accept":"application/json, text/event-stream"}
        if self._session:
            headers["Mcp-Session-Id"] = self._session
        if self._protocol:
            headers["MCP-Protocol-Version"] = self._protocol
        req = urllib.request.Request(self.endpoint, json.dumps(obj).encode(), headers, method="POST")
        try:
            with self._opener.open(req, timeout=15) as resp:
                status = resp.status
                sid = resp.headers.get("Mcp-Session-Id")
                raw = resp.read(MAX_BODY+1)
                media = resp.headers.get("Content-Type","").split(";")[0].strip().lower()
        except urllib.error.HTTPError as exc:
            raise TransportError("Fleet HTTP status "+str(exc.code)) from None
        except (OSError, ValueError):
            raise TransportError("Fleet transport failed") from None
        if len(raw)>MAX_BODY:
            raise TransportError("oversize response")
        if notification:
            if status not in (200,202,204):
                raise TransportError("notification rejected")
            return None
        if status != 200 or media != "application/json":
            raise TransportError("unsupported response format")
        try:
            body = json.loads(raw, object_pairs_hook=unique_object)
        except (ValueError, UnicodeError):
            raise TransportError("invalid JSON response") from None
        if (not isinstance(body,dict) or body.get("jsonrpc")!="2.0"
                or type(body.get("id")) is not int or body["id"]!=self._seq
                or "error" in body or not isinstance(body.get("result"),dict)):
            raise TransportError("invalid or rejected RPC")
        if sid:
            if not re.fullmatch(r"[!-~]{1,256}",sid) or (self._session and sid!=self._session):
                raise TransportError("invalid or changed session")
            self._session=sid
        return body["result"]

    def initialize(self):
        result=self._request("initialize",{"protocolVersion":"2025-11-25","capabilities":{},
                      "clientInfo":{"name":"fr3k-specops-read","version":"0.1.0"}})
        info=result.get("serverInfo")
        if not isinstance(info,dict) or info.get("name")!="fr3k-fleet-mcp":
            raise TransportError("unexpected server identity")
        protocol=result.get("protocolVersion")
        if protocol not in ("2025-11-25","2025-06-18","2025-03-26","2024-11-05"):
            raise TransportError("unsupported protocol")
        self._protocol=protocol
        self._request("notifications/initialized",{},notification=True)
        return {"server":info["name"],"protocol":protocol}

    def read(self, tool, job_id):
        if not self._protocol:
            raise TransportError("initialize first")
        if tool not in TOOLS or not isinstance(job_id,str) or not JOB.fullmatch(job_id):
            raise ValueError("unsupported tool or invalid job ID")
        args={"job_id":job_id}
        if tool=="fleet_command_status":
            args.update(wait_seconds=0,max_output_bytes=32768)
        result=self._request("tools/call",{"name":tool,"arguments":args})
        if result.get("isError") or not isinstance(result.get("structuredContent"),dict):
            raise TransportError("tool rejected or missing structured result")
        record=result["structuredContent"]
        if record.get("job_id")!=job_id:
            raise TransportError("receipt identity mismatch")
        return record

class Response:
    def __init__(self, body, status=200, media="application/json"):
        self.status=status
        self.headers={"Content-Type":media}
        self.raw=json.dumps(body).encode()
    def __enter__(self): return self
    def __exit__(self,*args): pass
    def read(self,n): return self.raw[:n]

class Fixture:
    def __init__(self): self.requests=[]; self.bad_id=False; self.bad_server=False
    def open(self,req,timeout):
        body=json.loads(req.data); self.requests.append(body)
        if "id" not in body: return Response({},202)
        if body["method"]=="initialize":
            result={"serverInfo":{"name":"other" if self.bad_server else "fr3k-fleet-mcp"},
                    "protocolVersion":"2025-11-25"}
        else:
            result={"structuredContent":{"job_id":body["params"]["arguments"]["job_id"]}}
        return Response({"jsonrpc":"2.0","id":body["id"]+int(self.bad_id),"result":result})

class Tests(unittest.TestCase):
    def setUp(self):
        self.fixture=Fixture()
        self.client=FleetReadClient("https://example.invalid/mcp","fixture-not-a-real-token",self.fixture)
    def test_read(self):
        self.client.initialize()
        self.assertEqual(self.client.read("fleet_jobs_status","a"*32)["job_id"],"a"*32)
        self.assertEqual(self.fixture.requests[-1]["params"]["name"],"fleet_jobs_status")
    def test_command_status(self):
        self.client.initialize(); self.client.read("fleet_command_status","b"*32)
        self.assertEqual(self.fixture.requests[-1]["params"]["arguments"]["wait_seconds"],0)
    def test_no_mutation(self):
        self.client.initialize()
        with self.assertRaises(ValueError): self.client.read("fleet_command_execute","a"*32)
        self.assertEqual(len(self.fixture.requests),2)
    def test_bad_endpoint(self):
        for ep in ("http://example.invalid/mcp","https://u:p@example.invalid/mcp","https://example.invalid/mcp?x=1"):
            with self.assertRaises(ValueError): FleetReadClient(ep,"fixture",self.fixture)
    def test_wrong_id(self):
        self.fixture.bad_id=True
        with self.assertRaises(TransportError): self.client.initialize()
    def test_wrong_server(self):
        self.fixture.bad_server=True
        with self.assertRaises(TransportError): self.client.initialize()
    def test_uninitialized(self):
        with self.assertRaises(TransportError): self.client.read("fleet_jobs_status","a"*32)
    def test_duplicate_json(self):
        with self.assertRaises(TransportError): json.loads('{"x":1,"x":2}',object_pairs_hook=unique_object)
    def test_invalid_job(self):
        self.client.initialize()
        with self.assertRaises(ValueError): self.client.read("fleet_jobs_status","not-a-job")

if __name__=="__main__":
    unittest.main(verbosity=2)
