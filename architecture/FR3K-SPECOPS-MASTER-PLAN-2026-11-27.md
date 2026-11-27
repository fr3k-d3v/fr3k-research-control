# FR3K SpecOps — master execution plan and candidate compilation
Date: 2026-11-27 | Plan ID: FR3K-SPECOPS-001 | Status: research / pre-implementation
Public-safe research coordination; no credentials, private infrastructure identifiers, or raw personal data. One Fleet authority; this is not another scheduler. Future canonical monorepo migration only after ownership verification.

## Mission
Connect machines. Measure reality. Delegate work. Verify results. Adopt Spec Kit as requirements/plan layer, extend rather than fork; Fleet owns execution, leases, authorization and scheduling; isolated Codex/OpenCode/Hermes/local agents implement; independent verifier evaluates actual state; GitHub preserves sanitized evidence. Retain local/self-hosted core free; hosting/coordination optional. OBSERVE → VERIFY → RECONCILE → IMPROVE → TEST → RECORD. Distinguish CLAIM, OBSERVATION, EVIDENCE, VERIFIED FACT, HYPOTHESIS, SIMULATION, UNKNOWN and BLOCKED. A commit is not deployment, heartbeat is not progress, simulation is not physical verification.

## Authoritative checklist
Only tick after linked evidence meets acceptance criteria; update this document via reviewed commit, not duplicate checklists. Stable IDs never reused. Record owner, dependency, attempt, evidence URL/hash, date, exit code, actual versus expected and blockers. Failed/blocked remain unticked; immutable attempt terminal results; retry as a new attempt. 
- [x] S00 Identify upstream Spec Kit and existing research coordination repository; README read via GitHub 2026-11-27 (blob a4ea4f520add603de250c59f96037f0eb7be46e5 for Spec Kit; 5ec04cd6c9134e4ba4048f34806bf1e242359024 for research control).
- [x] S01 Perform initial zero-star discovery and README triage; candidate register below. Not source or licence audit.
- [ ] S02 Inventory existing FR3K specifications, workflows, skills, job schemas and current deployment state; resolve ownership and canonical locations. Depends S00.
- [ ] S03 Pin upstream release/commit, check LICENSE and dependencies, verify integrity, record versioned CLI help and extension compatibility. Depends S00.
- [ ] S04 Audit P0 candidates: licence files/SPDX, provenance, dependency lockfiles, install scripts, hooks, network/filesystem permissions, security issues, tests. Capture commit SHA, not merely README blob. Reject unknown licences for copying; BSL reference-only until legal review. Depends S01.
- [ ] S05 Create FR3K constitution and preset (agent-neutral): requirements, test-before-completion, evidence hierarchy, privacy, authority, local-first and no competing orchestrator. Depends S02,S03.
- [ ] S06 Establish spec/plan/tasks/checklist/acceptance matrix and bug/assess/convergence workflows in isolated scratch repo. Verify exact supported commands from pinned CLI. Depends S05.
- [ ] S07 Define versioned job contract: spec ID, task ID, idempotency key, dependencies, worker capability, lease/fencing token, authority, timeout, budget, expected artifacts, rollback, cancellation and terminal state. Map to existing Fleet rather than replace. Depends S02,S05.
- [ ] S08 Build read-only Fleet adapter first; observe actual tool schemas and statuses, correlate job IDs; no secrets in logs. Depends S07.
- [ ] S09 Implement approval-scoped submit/status/cancel/evidence adapter; default OBSERVE, explicit AUTO/APPROVAL/PHYSICAL boundaries, deny unapproved commands, reject stale lease and replay. Depends S08.
- [ ] S10 Worker isolation: per-task worktree, clean sandbox, restricted credentials and network, resource limits, no privileged mounts; test cross-task contamination, cleanup and restart. Depends S04,S07.
- [ ] S11 Independent verification runner with deterministic unit/integration/runtime checks, red-green test evidence, negative cases, artifact digests, fresh context reviewer; model judgement supplemental only. Depends S06,S10.
- [ ] S12 Evidence schema: raw logs privately preserved before interpretation, sanitized public summaries, hashes, timestamps, source/build/artifact/deploy/device identity, test results and provenance; tamper-evident records plus independent signed checkpoint. Depends S07,S11.
- [ ] S13 Bounded convergence: compare requirements to observed behavior, create corrective tasks, rerun failures, stop on budget/deadline/repeated failures/authority denial; never self-approve or mark missing evidence passed. Depends S09,S11,S12.
- [ ] S14 Install agent integrations in scratch environments (Codex, OpenCode, Hermes, local agent); compare identical task, cost, latency, pass rate and portability; avoid replacing existing instructions. Depends S06,S10.
- [ ] S15 Implement proposed FR3K commands as extension/skills after interface review: discover, observe, reconcile, delegate, build, deploy, hardware, verify, converge, audit, release. Gate mutating tools at Fleet server. Depends S09,S13,S14.
- [ ] S16 CI and supply chain: pin actions/deps; secret scan, SBOM, licence policy, artifact attestation/signature, verify signature before install. Depends S12.
- [ ] S17 Pilot Fleet reliability: reproduction of enrollment/approval/lease/retry failures; test restart, offline worker, duplicate job and stale fencing. No production write until scoped authorization. Depends S13,S16.
- [ ] S18 Pilot firmware: reproducible build, binary digest, simulated tests labelled, authorized physical OTA and rollback, verify version after reboot, actual peripherals and voice, recovery procedure. Depends S17.
- [ ] S19 Pilot Android/SENTIENCE: verify package identity/version, preserve data, real device UI/voice/avatar/motion/overlay tests, crash and rollback evidence. Depends S17.
- [ ] S20 Pilot mobile AI and media: benchmark actual local inference and resource use, verify media generation/playback outputs and integrity, no model/asset redistribution without rights. Depends S17.
- [ ] S21 Pilot web/product release: staging smoke, deployment identity, health and rollback, separate source/build/deploy records. Depends S16,S17.
- [ ] S22 Publish sanitized reusable FR3K SpecOps preset/extension, docs, examples, versioned release; keep private control configuration separate. Depends S18–S21 (or document explicit scoped exclusions).
- [ ] S23 Build ongoing discovery pipeline (weekly and on demand): exact searches, zero-star queries, dedupe by repo ID, pin revision, provenance/licence gates, classify adopt/adapt/reference/reject, record negative results and recheck dates. Depends S04.
- [ ] S24 Final convergence audit: every requirement links to independent evidence or explicit blocker; test clean install, rollback, security and offline operation; record release decision. Depends S22,S23.

## Candidate register — initial compilation
P0 = evaluate first, P1 = complementary, P2 = research only. OBSERVATION means README/docs claim observed, not independently proven. All candidates uninstalled, unaudited, unapproved for execution. README blob IDs identify inspected content, not checkout commits. Zero-star means returned by GitHub query stars:0 on date, not a live count guarantee.

| ID | Repository | Tier | Evidence / reuse target | Decision |
|---|---|---|---|---|
| R01 | [github/spec-kit](https://github.com/github/spec-kit) | P0 | README blob a4ea4f520add603de250c59f96037f0eb7be46e5: SDD, convergence, bug and assess processes, reusable primitives | Adopt candidate, pin and test |
| R02 | [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) | P1 | Public docs: delta specs, proposal/design/tasks, skills and archive | Compare lightweight retrofit; no second source of truth |
| R03 | [odinhg/spectend](https://github.com/odinhg/spectend) | P0 zero-star | README blob 2c10dfc4f8de115788a8d3c1792f5050ad1e2593: parallel review, PR, retrospective, issue triage | Inspect review templates |
| R04 | [kkkkjack/proofrail-hermes](https://github.com/kkkkjack/proofrail-hermes) | P0 zero-star | README blob 4626369f8550c69c1bdc7b4ef9ae069f5c3f35c4: observe-before-edit, validate-after-mutation, context anchors, Hermes hooks | Test hook enforcement and bypass resistance |
| R05 | [Kausha3/mcp-evidence-recorder](https://github.com/Kausha3/mcp-evidence-recorder) | P0 zero-star | README blob 779328562d78dc748e579ed55bbb778de8ce0db0: HTTP sidecar, redaction, SQLite/hash chain, evidence exports; MIT claimed | Reference evidence schema; evaluate redaction and external checkpoints |
| R06 | [terok-ai/terok-executor](https://github.com/terok-ai/terok-executor) | P0 zero-star | README blob 41fbe695638e93292dcd04b9c7754b6ae395d22e: rootless Podman agent runtime; Apache-2.0 claimed | Sandbox spike on Linux; host credentials must remain isolated |
| R07 | [smallTechOrg/zero-shot-harness](https://github.com/smallTechOrg/zero-shot-harness) | P0 zero-star | README blob e8f6e4ec2fa7d435c2ef70ef24785c3d658f1edf: build/fix/sync skills, scaffold gate, real-service tests | Adapt gate concepts only after licence review |
| R08 | [techdeveloper-org/mcp-policy-enforcement](https://github.com/techdeveloper-org/mcp-policy-enforcement) | P1 zero-star | README blob c6b0398e6e948b0c044330740b567095a199f886: compliance state, flow trace, JSONL tool logs; MIT claimed | Reference policy trace; do not substitute for server-side auth |
| R09 | [niittymaa/multi-agent-ralph-loop](https://github.com/niittymaa/multi-agent-ralph-loop) | P2 zero-star | README blob 1eaff4d2ca2154dee232b5e827e58f5517fe1b6b: worktrees, adversarial review, model routing; BSL 1.1 claimed | Reference only; no code copying or deployment |
| R10 | [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | P1 | Public coding-agent evaluation guide: Codex/OpenCode SDK evaluation | Benchmark harness |
| R11 | [OpenHands/benchmarks](https://github.com/OpenHands/benchmarks) | P1 | Public docs: SWE-Bench and safety evaluation | Independent test tasks |
| R12 | [in-toto/attestation](https://github.com/in-toto/attestation) | P0 | Public specification: authenticated artifact metadata | Evidence interchange |
| R13 | [sigstore/cosign](https://github.com/sigstore/cosign) | P0 | Public docs: verify in-toto attestations | Artifact signing and verification |
| R14 | [labgrid-project/labgrid](https://github.com/labgrid-project/labgrid) | P0 | Public docs: embedded hardware abstraction, pytest integration | Physical test fixture candidate |
| R15 | [hastekit/agent-sdk-go](https://github.com/hastekit/agent-sdk-go) | P2 | Public docs: Temporal/Restate durable execution, OTel tracing | Reference retry semantics, no new orchestrator |
| R16 | [diarized/spec-beads](https://github.com/diarized/spec-beads) | P2 zero-star | Search hit; README.md returned 404 | Inspect tree/alternate README; UNKNOWN |
| R17 | [Armaan-khan786/esp32-uart-ci](https://github.com/Armaan-khan786/esp32-uart-ci) | P2 zero-star | Search hit; README.md returned 404 | Inspect tree; UNKNOWN |
| R18 | [GenieRobot/spec-kit-maqa-github-projects](https://github.com/GenieRobot/spec-kit-maqa-github-projects) | P2 zero-star | Search hit only | GitHub Projects sync candidate |
| R19 | [HBM1990/multi-agent-verification-workflow](https://github.com/HBM1990/multi-agent-verification-workflow) | P2 zero-star | Search hit only | Independent verifier patterns |
| R20 | [unbound-force/replicator](https://github.com/unbound-force/replicator) | P2 zero-star | Search hit only | Worktree/agent isolation candidate |
| R21 | [taagarwa-rh/agent-worktrees](https://github.com/taagarwa-rh/agent-worktrees) | P2 zero-star | Search hit only | Worktree management |
| R22 | [wozqhl/mcp-gateway](https://github.com/wozqhl/mcp-gateway) | P2 zero-star | Search hit only | Gateway policy patterns |
| R23 | [jcorrego/mcp-policy-gateway](https://github.com/jcorrego/mcp-policy-gateway) | P2 zero-star | Search hit only | Gateway authorization patterns |
| R24 | [raws-labs/srig-templates](https://github.com/raws-labs/srig-templates) | P2 zero-star | Search hit only | Hardware-in-loop candidate |
| R25 | [helonayala/esp32_daq](https://github.com/helonayala/esp32_daq) | P2 zero-star | Search hit only | Hardware measurement candidate |

### Additional research queue (not verified in this pass)
obra/superpowers; steveyegge/beads; agentskills/agentskills; open-policy-agent/opa; temporalio/temporal; restatedev/restate; opentelemetry/opentelemetry-collector; espressif/pytest-embedded; pytest-dev/pytest; google/osv-scanner; anchore/syft; gitleaks/gitleaks; modelcontextprotocol/inspector; microsoft/playwright; appium/appium. Confirm current upstream canonical names, docs, licence and compatibility before use.

### Search reproducibility
GitHub repository searches: `spec-driven development stars:0 fork:false`; `spec-kit extension stars:0 fork:false`; `agent workflow verification stars:0 fork:false`; `agent sandbox stars:0 fork:false size:>30`; `coding agent worktree stars:0 fork:false size:>20`; `hardware in loop esp32 stars:0 fork:false size:>10`; `mcp policy audit stars:0 fork:false size:>20`. First 8–12 results per query, selected relevant candidates; not exhaustive. Public docs: https://github.com/Fission-AI/OpenSpec/blob/main/docs/overview.md ; https://github.com/promptfoo/promptfoo/blob/main/site/docs/guides/evaluate-coding-agents.md ; https://docs.sigstore.dev/cosign/verifying/attestation/ ; https://github.com/in-toto/attestation ; https://github.com/labgrid-project/labgrid ; https://github.com/OpenHands/benchmarks.

## Compilation protocol / next executable batch
Do not install untrusted code on production. Clone pinned commits into disposable restricted workspaces only after review; record URL, revision, license file hash, dependency inventory, commands, tests, risk, applicable files, integration decision and evidence. Prefer clean-room patterns or upstream dependency over copying. No secrets in environment/logs. Keep source and build artifacts separate. First batch: R01, R03–R07, R12–R14; S02/S03/S04 parallel read-only; S05 after observations. Build the smallest preset plus test fixtures, then adapter, then pilot. Actual compilation/builds and device deployments have NOT started. No new runtime or repository ownership migration approved by this document.
