# FR3K SpecOps — research implementation
This directory contains an additive Spec Kit preset, native observation/convergence extension, pure task and receipt validation, bounded corrective proposals and a standalone read-only Fleet transport. It is not a production scheduler or release authority.

## Reproducible local checks
Python 3.11+; all four module test suites use the standard library. Run from repository root:
```sh
python3 -I -B specops/contract.py
python3 -I -B specops/fleet_observe.py
python3 -I -B specops/converge.py
python3 -I -B specops/fleet_transport.py
```
Pinned Spec Kit 1.4.5 was installed into a restricted disposable directory and tested offline. Native integration assets were registered for Codex and OpenCode, not installed over existing user configuration. Install only in a new scratch project with the approved pinned dependency set. See the [master plan](../architecture/FR3K-SPECOPS-MASTER-PLAN-2026-11-27.md) for audit gaps.

## Standalone read-only transport
An operator must provision a dedicated short-lived OAuth grant limited to `fleet.read` through the gateway's supported consent flow. The existing ChatGPT connector grant is not a credential transferable to arbitrary scripts. Never paste credentials into GitHub, chat, shell commands or logs. Use a trusted local process to supply the token at runtime. The client intentionally does not search for credentials, request wider scopes, or automate operator consent. The gateway is responsible for verifying scope and identity.

Example from the specops directory (trusted local terminal only):
```python
from getpass import getpass
from fleet_transport import FleetReadClient
from fleet_observe import observe
endpoint = input("Authorized HTTPS MCP endpoint: ")
job_id = input("Existing Fleet job ID: ")
client = FleetReadClient(endpoint, getpass("Short-lived read grant: "))
client.initialize()
result = observe(job_id,
                 lambda j: client.read("fleet_jobs_status", j),
                 lambda j: client.read("fleet_command_status", j))
print(result)
```
The prototype accepts JSON MCP replies and rejects other reply formats, redirects, unexpected server identity, mismatched IDs and missing structured results. It is deliberately limited to the two receipt tools. HTTPS and agreement between receipts do not prove that a receipt is signed or that requirements passed. Output remains non-authoritative. Positive authenticated standalone acceptance is pending a dedicated read grant; a live invalid-token rejection test passed. Mock tests do not substitute for positive production authentication.

## Authority and release
The existing Fleet orchestrator owns dispatch, approval, leases, fencing, dependencies, cancellation, immutable receipts and release authorization. Never infer permission from this repository. Any future submission adapter must be reviewed against actual server-side authority contracts, and cannot bypass them.
