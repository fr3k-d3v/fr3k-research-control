# Fleet delegation and authority

One authoritative orchestrator owns job IDs, dependency graph, device capabilities, leases, fencing tokens and immutable terminal states. Workers may execute only explicitly scoped jobs. Assign Omarchy GPU-exclusive inference/benchmark work; Contabo CPU/network research, emulation and coordination; X1 compatible auxiliary tasks. Never dispatch to retired Parrot.

Authority classes: OBSERVE (read only), AUTO (bounded reversible work), APPROVAL (explicit operator decision), PHYSICAL (hardware/device effects). A device connection approved once may receive a **device-bound one-hour lease**; this is a requested policy, not evidence of deployment. A lease must expire, be revocable and never bypass authorization for destructive or physical operations. No repeated approval for already-authorized routine local Omarchy work, but do not bypass existing enforcement without verifying policy.

Approval UX: when an actual pending request exists, show one copyable Termux block that SSHes to Contabo and executes the exact Fleet approval command with the real request ID. Never invent commands or approve unknown/expired requests. Redact keys and private host details from public artifacts.

Scheduling: CPU research can continue while GPU acceptance owns the exclusive lease. Use stable idempotency keys, lease renewal, timeout, worker heartbeat plus actual progress evidence, retries with backoff and explicit BLOCKED status. Failed tests preserve raw evidence and trigger rollback. Do not mistake a process heartbeat for job completion.
