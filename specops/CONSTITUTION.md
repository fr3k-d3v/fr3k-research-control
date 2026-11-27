# FR3K SpecOps constitution — draft v0.1
Normative design proposal; not deployed. The existing Fleet authority and ecosystem work register remain authoritative. This document must never grant privileges.

## Principles
1. Reality before claims: OBSERVE → VERIFY → RECONCILE → IMPROVE → TEST → RECORD. Label claims, observations, evidence, verified facts, hypotheses, simulations, unknowns and blockers. Preserve raw evidence privately; sanitize before publication.
2. Requirements before implementation: stable requirement/task IDs; every requirement specifies observable acceptance criteria and required evidence kind. Version changes explicitly and bind receipts to the task digest. No retroactive weakening to make a test pass.
3. One execution authority: Fleet owns worker identity, command authorization, job leases, fencing, idempotency, dependency state, receipts, retry and cancellation. SpecOps is a specification and verification client only. Do not introduce a second scheduler or grant permission from local files.
4. Authority is fail-closed: OBSERVE read-only; AUTO bounded/reversible within a verified grant; APPROVAL requires scoped operator authorization; PHYSICAL effects require device-specific policy and authorized physical acceptance. A physical kill switch is a separate overriding denial, not a permission. Never infer live authority from a README.
5. Isolate workers: one worktree per task, restricted credentials, network/filesystem/resource boundaries, no unreviewed hooks, no shared production secrets, clean environment. Pin and audit dependencies; unlicensed source is reference-only without copying.
6. Independent verification: collect actual source, build, runtime, deployment, physical and rollback evidence separately. Compiler success cannot substitute for runtime, simulated hardware cannot substitute for real hardware. Verifier identity and receipt must be authenticated independently; structural checks alone never promote anything.
7. Bound convergence: require an attempt limit, timeout and resource budget; stop on repeated failure, authorization refusal, budget exhaustion, absent evidence or unsafe state. Retry with a new attempt ID; terminal results immutable. Record negative results.
8. Publish responsibly: local-first free core; keep private control configuration and evidence separate. Signed release artifacts, reviewed dependency licences, reproducible builds and rollback tests are mandatory when relevant.

## Feature workflow
- Constitution → specification → clarify → plan → tasks → acceptance checklist → implementation → convergence → independent verification → record.
- Each task has one owner, canonical ID, dependencies, authority, capability, expected evidence, timeout and idempotency key.
- Every task claim and result belongs in the existing work register and owning issue/PR; no separate dispatch authority.
- Use upstream Spec Kit v1.4.5 only after dependency review and restricted CLI testing. Integrate native preset/extension schemas from pinned documentation, not guessed commands.
- Proposed extension commands: discover, observe, reconcile, delegate, build, deploy, hardware, verify, converge, audit, release. All mutating commands must go through Fleet's actual authorization interface.

## Initial executable contract
Run `python3 -I -B specops/contract.py` from repository root. Standard library only; runs synthetic unit tests, no device interaction. Contract v1 checks task structure, graph dependencies, duplicate idempotency keys, timeout, evidence type, digest, independent role identifiers, simulation flag and exit code. A structurally valid receipt still returns authenticated=false and promotion_authorized=false. Trusting caller-supplied identifiers/digests would be unsafe. A later read-only adapter must obtain and authenticate authoritative Fleet records and verify artifacts against private evidence; a separate release authorization policy must be evaluated server-side.

## Required future adapter contract
Read observed Fleet schema before implementation. Map spec/task ID to real Fleet job ID and attempt; distinguish request/approval/job/receipt identifiers. Preserve immutable terminal records, fencing and lease expiry. Check server-side authorization, device identity, artifact digest, dependency receipts and verifier identity. Deny on unknown fields, unsupported capabilities, expired grant, missing provenance, stale report, offline physical device, or unverified rollback. Never cache authorization beyond the server grant. Production rollout requires canary, test results and rollback evidence.
