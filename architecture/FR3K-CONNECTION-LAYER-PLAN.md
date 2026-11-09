# FR3K Connection Layer — research-backed architecture and implementation plan

**Date:** 2026-11-09 AEST. **Status:** PROPOSAL, not deployed. **Decision:** extend the existing Fleet MCP control plane; do not build a competing orchestrator. GitHub is authoritative public engineering record; private source/evidence remains private. Parrot retired, Omarchy active.

## Executive decision
Build **FR3K Fabric**, a secure, durable connection and execution layer that separates identity/transport, authority, orchestration, execution, artifacts and verification. The system must survive disconnects, retries, crashed workers, stale leases and conflicting job submissions without double execution. A heartbeat is not evidence of progress; a successful process exit is not necessarily task correctness.

## Observed baseline and gaps
- OBSERVED: Omarchy RTX3060 runs a 65,536-context Qwen3-Coder 30B MoE via llama.cpp; acceptance is in cache isolation as of 18:02 AEST, with remaining gates. Do not contend for GPU before it completes.
- OBSERVED: Fleet MCP can reach Contabo and Omarchy; a Contabo Gitea instance responds on localhost:3000, but anonymous API returns HTTP 403. No authenticated mirror proven.
- OBSERVED: GitHub org contains at least 21 repositories at 17:54 AEST. Public research-control and private GPU source repositories exist; no proof of scheduled sync or full monorepo consolidation.
- UNKNOWN: network topology and tailnet grants, worker credential rotation, device capability completeness, X1 uptime, emulator isolation, physical test automation readiness, Gitea auth route. Audit before production changes.

## Layered design
1. **Identity + transport:** Tailscale/SSH or authenticated mutually verified TLS as appropriate; explicit per-device identity, narrowly scoped grants, no public inbound worker port by default. Network reachability never implies execution authority.
2. **Control API:** existing Fleet MCP as adapter into a single orchestrator. Versioned contracts for register, heartbeat, capabilities, submit, inspect, cancel, approve, lease, attest, artifact and event. No direct arbitrary shell from untrusted agent prompts.
3. **Durable authority and state:** PostgreSQL on Contabo, one transactionally authoritative job/event store. Explicit job graph, idempotency keys, fencing epochs, state transitions, deadlines, retries, approval ledger and terminal immutability.
4. **Dispatch:** start with Postgres transactional outbox + worker polling (lowest integration risk). Evaluate NATS JetStream for multi-worker durable transport after failure tests; it is at-least-once, so consumers MUST be idempotent. Temporal is a later alternative for durable workflows, not a second concurrent source of truth.
5. **Workers:** isolated adapters for Omarchy GPU, X1 builds, Contabo emulation, Android ADB/Termux and firmware boards. Each worker advertises measured capabilities and accepts bounded typed tasks, not unrestricted authority.
6. **Artifact/evidence:** content-addressed object storage for raw logs, APKs, video scene outputs, benchmark JSON, crash traces and firmware images; digest/size/provenance recorded in Postgres. GitHub stores sanitized source, manifests, tests and reports; private repository holds sensitive implementation, never secrets.
7. **Telemetry:** OpenTelemetry traces/metrics/log correlation by job_id, attempt_id, worker_id, device_id and artifact digest. Explicit verified outcomes, not just uptime.

## Protocol contracts (draft)
`Device`: device_id, public_identity, hardware_inventory, capabilities[], trust_state, last_seen_at, policy_version, health_observations[].
`Job`: job_id(UUIDv7), idempotency_key, parent_id, kind, typed_input_ref, dependencies[], priority, resource_claims, authority_class, policy_version, deadline, state, created_at.
`Lease`: lease_id, job_id, device_id, resource_id, fencing_token(monotonic), issued_at, expires_at, renewable, policy_version.
`Attempt`: attempt_id, job_id, lease_id, started_at, heartbeat_at, progress_evidence_ref, exit_code, verification_result.
`Artifact`: sha256, media_type, bytes, producer_attempt_id, raw_or_derived, storage_ref, visibility, retention_policy.
`Approval`: request_id, exact_action_digest, actor, device_id, scope, issued_at, expires_at, revoked_at, audit_event_ref.

Allowed states: PROPOSED -> QUEUED -> LEASED -> RUNNING -> VERIFYING -> SUCCEEDED or FAILED; BLOCKED and CANCELLED explicit terminal/controlled transitions. Never rewrite terminal outcome; create a new job for retry. Late worker result with old fencing token is rejected.

## Approval and trust
OBSERVE read-only; AUTO bounded reversible operations; APPROVAL privileged/destructive/publishing; PHYSICAL firmware flashing and physical side effects. Requested one-hour **device-bound connection approval lease** applies only to explicitly approved connection scope, never blanket permission for dangerous commands. Approvals expire and revoke. Use actual pending job ID in one copyable Termux SSH+approve block; never fabricate commands or bypass controls. Store no access tokens in Git, manifests, command output or traces.

## Hardware routing
- Omarchy: exclusive GPU resource with VRAM budget; coding inference, benchmarks, video segmentation and encode queues. GPU experiments serialized; CPU-only research can coexist under I/O/RAM budgets.
- Contabo: orchestrator, Postgres, research scans, artifact indexes, Gitea mirror, Android emulation (CPU budgeted), API gateway; not assumed to have NVIDIA GPU.
- X1: auxiliary builds, QA, media jobs subject to verified inventory and availability.
- OnePlus 7 Pro/7, Fold4: real Android acceptance, mic/overlay/rotation/foldable tests; explicit device leases and ADB trust.
- K230, K10, Tab5, T-Deck Plus, T-Beam and other ESP32: firmware build/test; flash requires PHYSICAL approval; verify boot and communications before success.

## Three flagship end-to-end workflows
**Overlay:** content ID -> 22-scene DAG -> segmentation on Omarchy -> alpha integrity tests -> APK packaging -> Contabo emulator -> phone smoke/fold/voice tests -> signed release gate. Each failed green-mask, wrong rotation, queue-order or mic-crash bug becomes a regression test.
**Local coding optimization:** research source+SHA -> compatibility/security review -> wait for current GPU acceptance -> reserve exclusive lease -> four-arm A/B/C/D cache/placement experiment at 4K/16K/64K -> correctness/tool-call/long-context -> latency, watts, VRAM and recovery -> candidate approval/rollback.
**Firmware/Reticulum:** discover exact board -> architecture/pinout/firmware compatibility -> build and simulated checks -> PHYSICAL approval -> flash -> verify boot, radio connectivity, recovery, current draw -> evidence record.

## Alternatives and decisions
| Concern | Option | Recommendation and trade-off |
|---|---|---|
| Transport | Fleet MCP over existing secure connection | Keep as compatibility API; no new control plane |
| Queue | Postgres outbox + polling | First implementation: fewer moving parts, transactional state; polling overhead acceptable |
| Queue growth | NATS JetStream | Later, after failure testing; durable at-least-once delivery means dedup required |
| Workflow engine | Temporal | Later evaluation; excellent durable replay but operational overhead and potential duplicate orchestration |
| Network | Tailscale grants + tags | Prefer deny-by-default least privilege; audit current tailnet before editing |
| Observability | OpenTelemetry | Cross-language trace context; avoid secrets in attributes |
| Git sync | GitHub authoritative -> Gitea mirror | One-way, signed/verified hashes; block until authenticated Gitea API available |

## Milestones with exit criteria
**M0 (1-2 days engineering estimate):** snapshot fleet/permissions/active jobs; freeze accepted GPU baseline; inventory all GitHub and Gitea repositories and service contracts. EXIT: signed-off state map and no contradictory sources of truth.
**M1 (3-5 days):** schema, migrations, job state machine, idempotency, leases/fencing and typed API behind existing Fleet MCP. EXIT: tests prove no double-execution on retry, stale result rejected, terminal immutability.
**M2 (3-5 days):** Omarchy and Contabo worker adapters, capability registry, GPU exclusive lease, artifact digests, tracing. EXIT: disconnect/reconnect and crash injection pass; GPU acceptance untouched.
**M3 (4-7 days):** overlay DAG + Android emulator + one real phone, regression test catalog. EXIT: one creature-to-APK path with independently verified artifact and crash capture.
**M4 (4-7 days):** continuous research import, candidate ledger, A/B/C/D benchmark queue, safe rollback. EXIT: one reproducible measured optimization with negative controls.
**M5:** X1, remaining phones and firmware boards, voice front end, dashboard, release automation. EXIT: verified multi-device workflow and audit trail.
Estimates are engineering hypotheses, not commitments; hardware availability, credentials and current acceptance may alter schedule.

## Mandatory failure tests
Disconnect during execution; expired/revoked connection approval; lost ack and redelivery; worker restart; duplicate submit; stale fencing token; missing artifact; failed integrity hash; out-of-disk; GPU OOM; runaway thermal; malformed tool call; dependency failure; emulator false-positive; Android mic crash; Gitea mirror drift; private-to-public leak attempt. Fail closed, record raw evidence, restore baseline.

## Source-backed research
- NATS JetStream delivery and durability: https://docs.nats.io/concepts/jetstream (at-least-once; not exactly-once execution).
- Temporal durable workflow model: https://docs.temporal.io/workflows and https://docs.temporal.io/tasks (event history/replay; evaluate only after core stability).
- Tailscale grants and tags: https://tailscale.com/docs/features/access-control/grants and https://tailscale.com/docs/features/tags (least privilege; identity is not job authorization).
- OpenTelemetry semantic conventions: https://opentelemetry.io/docs/concepts/semantic-conventions/ (cross-component correlation).
- FR3K local research: `FR3K-HARDWARE-MAXIMIZATION-SCOUT`, `FR3K-RESEARCH-STAGING-2026-11-09`, `FR3K-EXTERNAL-RESEARCH-2026-11-09`; these are mutable local notes, not verified benchmarks.

## Immediate next engineering actions
1. Audit Fleet MCP existing job/approval/lease schema and Contabo Gitea auth without exposing credentials.
2. Open tracked issues for M0-M5; use a single accountable orchestrator and explicitly assigned workers.
3. Prototype Postgres schema/state-machine and adversarial unit tests in private code repo, then publish sanitized architecture.
4. Do not interrupt current GPU acceptance. Gate optimization on its final exit and preserve failure evidence.
5. Verify GitHub private-source access and Gitea mirroring with SHA comparison; never assert sync without it.
