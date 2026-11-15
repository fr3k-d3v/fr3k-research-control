"""Read-only long-context acceptance probe for llama.cpp.

Explicitly opt-in. Reads key from environment only. Does not modify services.
Output is JSON with metrics and no prompt or credential contents.
"""
import argparse
import json
import os
import time
from urllib.request import Request, urlopen

def request_json(url, payload, key, timeout):
    req = Request(url, data=json.dumps(payload).encode(),
                  headers={"Authorization": "Bearer " + key,
                           "Content-Type": "application/json"})
    with urlopen(req, timeout=timeout) as resp:
        return json.load(resp)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--url", default="http://127.0.0.1:8080")
    p.add_argument("--model", default="fr3kc0d3r")
    p.add_argument("--target-tokens", type=int, default=64000)
    p.add_argument("--reserve", type=int, default=256)
    p.add_argument("--timeout", type=int, default=300)
    args = p.parse_args()
    key = os.environ.get("FR3K_LOCAL_API_KEY")
    if not key:
        p.error("FR3K_LOCAL_API_KEY required")
    if not 1024 <= args.target_tokens <= 65536 - args.reserve:
        p.error("target exceeds safe capacity")
    marker = "FR3K_CTX_BOUNDARY_83517"
    phrase = "alpha beta gamma delta epsilon. "
    def make(n):
        text = phrase * n
        midpoint = len(text)//2
        return text[:midpoint] + "\nMarker: " + marker + "\n" + text[midpoint:] + "\nReturn marker exactly."
    lo, hi = 1, 20000
    for _ in range(17):
        mid = (lo+hi)//2
        content = make(mid)
        result = request_json(args.url.rstrip("/") + "/tokenize", {"content":content}, key, 30)
        length = len(result["tokens"])
        if length <= args.target_tokens:
            lo = mid + 1
        else:
            hi = mid - 1
        if lo > hi:
            break
    content = make(max(1, hi))
    prompt_tokens = len(request_json(args.url.rstrip("/") + "/tokenize", {"content":content}, key, 30)["tokens"])
    if prompt_tokens > args.target_tokens:
        raise RuntimeError("token budget exceeded")
    start = time.monotonic()
    response = request_json(args.url.rstrip("/") + "/v1/chat/completions",
                            {"model":args.model,"messages":[{"role":"user","content":content}],
                             "max_tokens":32,"temperature":0}, key, args.timeout)
    elapsed = time.monotonic() - start
    answer = str(response["choices"][0]["message"].get("content", ""))
    print(json.dumps({"target_tokens":args.target_tokens,"raw_tokens":prompt_tokens,
                      "reported_prompt_tokens":response.get("usage",{}).get("prompt_tokens"),
                      "marker_correct":marker in answer,"elapsed_s":round(elapsed,2),
                      "finish_reason":response["choices"][0].get("finish_reason")}))
    if marker not in answer:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
