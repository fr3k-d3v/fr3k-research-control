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

## Execution record — 2026-11-27, pass 2
**VERIFIED FACT:** Read-only Fleet preflight exited 0 on an authorized Linux worker. Git, Python, uv, Docker, Codex and OpenCode are available; Specify was not found on PATH. This does not establish that every agent can authenticate or run. Initial acquisition attempt failed at Git initialization with disk quota exceeded (exit 128); no data deleted. Retried on an alternate CPU node with adequate reported storage; acquisition exited 0. Independent manifest readback matched SHA-256 `72542ba7277661dbf2568310f66b68685f0f23c0d8e7ee7ad7a494ba2522dd12`. Private workspaces and identifiers omitted from this public record. No upstream hooks, installers, builds, or code executed.

### S02 inventory (partial)
- [x] Read existing research operations, experiment and Fleet authority documents. Preserve current baseline and exclusive resource leases.
- [x] Identify existing ecosystem master work register: reuse it as the shared index; this plan is a subordinate feature checklist, not a new scheduler or task-claim authority.
- [x] Inspect existing product-level research collector; reuse its bounded metadata/tree/README/licence collection pattern rather than create redundant collectors.
- [x] Observe live Fleet device enumeration and worker preflight. Availability is not functional acceptance.
- [ ] Reconcile deployed version and full job/approval/receipt schema, resolve task ownership and existing work-register linkage through reviewed change.
- [ ] Normalize authority vocabulary carefully: physical-effect permission and a physical kill switch are distinct concepts; never map a kill-switch state to permission for remote action.

### S03 upstream pin (partial)
- [x] Select stable v1.4.5 from observed v1.4.x refs; annotated tag object `448b778d2605883621b2f10d131934c073ef9734`, peeled commit `6ba8beefff8d6408cadd62038e92d459093e33a8`. Main pyproject reports dev version; do not use it as release.
- [x] Read pinned LICENSE (MIT; blob `28a50fa22639e32febe14e4ffc7a732b0ba8c90a`) and pinned pyproject (blob `902e4502ea45422f7067a52293d3cc735fa3d8a5`), confirming 1.4.5 and Python >=3.11. Direct dependencies declared: typer, click, rich, readchar, pyyaml, packaging, pathspec, json5, mcp, pydantic, lark; hatchling build backend. No root uv.lock in inspected tree.
- [ ] Validate tag provenance/signature where available, resolve and audit transitive dependencies, inspect build/install scripts and upstream CI, run pinned CLI in clean restricted environment and record version/help/integration compatibility. No global installation.

### S04 source acquisition (partial)
- [x] Fetch exact commits into isolated no-checkout Git repositories; verify FETCH_HEAD against each pin, generate file-tree inventory and dependency/licence path list. 9/9 successful; manifest readback matches.
- [x] Inspect candidate root licence evidence and tree paths. No permission to copy code inferred from README alone.
- [ ] Review pinned licence contents, source, hooks, execution permissions, dependencies, vulnerabilities, tests and integration fit; record source audit and verdict per candidate. Execute tests only in suitable disposable restricted environment.

| ID | Pinned commit | Tree files | Preliminary licence evidence / gate |
|---|---|---:|---|
| R01 | `6ba8beefff8d6408cadd62038e92d459093e33a8` | 1072 | MIT at pin; audit dependency graph and CLI |
| R03 | `bcf40a963178688fd23c5246ca07df05a4fc0046` | 70 | No licence path found; BLOCKED for code reuse |
| R04 | `d4f1168ba0ff127e4297cd8f9132d8bbd3bfe5d8` | 33 | MIT file read on default branch; pinned LICENSE/plugin.yaml/pyproject paths present; recheck pin |
| R05 | `9f93558b473db9f70c8b53f1eb1bb7cb09d260b4` | 42 | MIT file read on default branch; pinned LICENSE, package-lock, requirements and pyproject present |
| R06 | `b4c03efef373f8084b5fafc969402c6d7ac3efa6` | 220 | Apache-2.0 file read on default branch; pinned LICENSE, uv.lock, pyproject present |
| R07 | `d48e79d9ebee0acb57781c38dbdaf1394ff654c3` | 34 | No licence path found; BLOCKED for code reuse |
| R12 | `50bf01716982189898823e90586075f37cd9bb7d` | 202 | Apache-2.0 file read on default branch; pinned LICENSE and Go/JS/Python/Rust manifests present |
| R13 | `fd42a8ca2855fe1fa50034133ecb10bdb88efdfd` | 478 | Apache-2.0 file read on default branch; pinned LICENSE, go.mod, go.sum present |
| R14 | `cfb48139d7daeb69d739439eb55ccf694abfb637` | 451 | LGPL-2.1-or-later header observed on default branch; pinned COPYING/LICENSE/pyproject present; verify exact obligations |

**Decision:** S02/S03/S04 remain open. The acquisition and version-selection subtasks are complete; full audit, dependency integrity and executable testing are not. Next: inspect pinned source in read-only mode, resolve licence gaps without copying, draft preset only after authority mapping; use a disposable build runner with no production credentials. Do not deploy to the gateway or hardware.

## Execution record — 2026-11-27, pass 3
**VERIFIED FACT:** Original offline task/receipt validator committed at `41f19ad3cc0cfc060e3882f60e3744700cab4f60`, [contract.py](../specops/contract.py), blob `1f34cacae2629d1cbd81ceb8c6249c27c4ae9345`. Standard-library unit suite passed 15/15 twice (including running the exact GitHub-readback source); both invocations exit 0. Fixtures are synthetic, not production or physical acceptance. Structural results explicitly deny authentication and promotion; no scheduler, shell execution or authorization implementation. Constitution draft at `1e1d27d8a54102433790fb97f6aaf10071a11164`, [CONSTITUTION.md](../specops/CONSTITUTION.md).
- [x] Read pinned licence headers for R04/R05/R06/R12/R13/R14 and selected Python manifests. MIT (R04,R05), Apache-2.0 (R06,R12,R13), LGPL-2.1-or-later (R14). No licence discovered R03/R07; no code copied. Full dependency/source/security audit still open.
- [x] Confirm Proofrail declares no runtime dependencies in its own pyproject; host Hermes integration remains unverified. Terok needs Podman and its sandbox/util dependencies. No assumption that Docker availability implies usable runtime.
- [x] Verify a clean Bubblewrap sandbox on Linux: no host home exposed, clear environment, isolated network connection attempt failed as expected. Docker API access denied to current worker; no privilege escalation.
- [x] Resolve Spec Kit 1.4.5's 42-package wheel-only dependency set with hashes inside restricted workspace. Initial TLS native-cert configuration failed; retry using default trust store succeeded, not insecure TLS. Lock SHA-256 `0d647daa69725c6173d65bdbfa68076bcdbf83bd03255c1097288a33917a350f`; full private lock retained. Vulnerability/licence/provenance review still pending. PyPI release artifact not yet independently matched to source pin.
- [x] Draft constitution, authority mapping, offline task/receipt contract, dependency validation and negative tests. Verified 15/15 synthetic tests; no authenticated Fleet receipt validation. S05, S07, S11 remain open pending native Spec Kit preset, full schema mapping and real verifier.
- [ ] Install hashed wheels in isolated workspace (Fleet package-change approval required; request pending, no install performed). After operator approval: verify package/version/provenance, run CLI in offline sandbox, initialize scratch project and test integrations without overwriting existing work.
- [ ] Complete security scan, source audit, authenticated Fleet adapter and all live/physical pilot gates. Do not tick top-level gates until acceptance evidence is linked.
**Decision:** Keep acquisition, prototype and actual deployment separate. No package installed globally, no production changes, no physical verification. Pending approval details are provided privately to the operator rather than in this public plan.

## Execution record — 2026-11-27, pass 4
- [x] Approved isolated installation: 42 hash-locked wheels, terminal exit 0. Independent CLI help test confirmed Specify 1.4.5.
- [x] Offline scratch initialization succeeded for Codex and OpenCode; bundled bug and assess extensions installed in Codex scratch project.
- [x] Native preset committed in `specops/preset/`; exact GitHub readback tested with both integrations. Both composed templates preserved core content and appended FR3K evidence gates. Artifact registration verified, terminal exit 0.
- [x] Corrected initial test assertion: preset resolve reports composition paths, while resolve_content returns the composed text.
- [ ] Full package provenance and dependency security reviews, preset conflict/removal tests, actual agent execution, Fleet integration and physical acceptance remain open. No production deployment or global installation. No new licence declared pending owner decision.

## Execution record — 2026-11-27, pass 5
- [x] Read actual Fleet job status and command status schemas from authenticated connector. Observed success, failure and approved installation receipts. These responses do not expose signed receipt, fencing or lease provenance; those remain unresolved.
- [x] Implement read-only reconciliation in specops/fleet_observe.py (commit 8908d986ce4ef24d1231bf8629c321af32bf0a77, blob 45899562140ebdffa8e8d4b9a47d00d907d8c203). Compare identity, device, state, exit code, terminal flag, approval requirement, truncation and timing; hash complete output. Never grant promotion or claim cryptographic authentication. Unknown or incomplete evidence fails closed.
- [x] Test GitHub-readback adapter: 10/10 unit tests plus three real Fleet response pairs (two successful executions and one failed execution), all correctly classified. Terminal verifier run exit 0. Actual harmless runtime marker observed. This tests connector-fed records, not a standalone authenticated MCP client.
- [x] Actual Codex invocation, read-only ephemeral scratch session, exit 0: given synthetic physical requirement with only compilation evidence, agent returned exactly BLOCKED: R1 missing physical evidence. Independent exact-output check passed. This is a model classification canary, not a physical test or a full agent implementation run.
- [x] Native read-only Spec Kit extension committed in specops/extension/. Scratch install and command registration passed 2/2 (Codex skill and OpenCode command), verified from GitHub readback. No production agent configuration altered.
- [ ] S08 remains open: wire authenticated transport into a reusable runtime client; verify live command invocation inside agent, signed/authoritative receipt provenance and version mapping. S09 mutating adapter must use actual server authorization and must not implement a competing approval mechanism.
- [ ] S14 remains open: full comparable agent workflows, actual OpenCode/Hermes invocation, resource and performance evaluation. S17-S24 live and physical acceptance remain open.

## Execution record — 2026-11-27, pass 6
- [x] Implement deterministic bounded convergence proposals in [specops/converge.py](../specops/converge.py), commit `75e28b2af299aa6a26ad73ec3006feaf1851f985`, blob `27e959bcda9ae387059471c05862c08527c136b2`. Exact GitHub-readback source passed 15/15 unit tests, exit 0. Existing contract and observation suites total 40 unit tests across the three modules. No new scheduler; planner has no I/O, dispatch or promotion authority.
- [x] Connector-mediated controlled failure/correction canary: first actual runtime command failed with exit 1; independently retrieved status and output matched; planner generated deterministic corrective proposal. Operator-authorized chat workflow submitted a separate harmless correction canary; second actual command exited 0 with expected exact marker. Independent re-observation and verification passed, requiring REVIEW_REQUIRED; a remaining failure at the attempt limit produced BLOCKED. Distinct actual attempts; not an unattended agent loop or physical test.
- [x] Native extension v0.2.0: receipt + converge commands, manifest commit `0708ef532f6441bf00d558373e0796558c568998`. Exact GitHub readback initialized in offline scratch projects; both commands registered in both Codex and OpenCode (4/4 registration checks; terminal exit 0).
- [ ] OpenCode actual model canary BLOCKED: default free model and alternative beam-free both reported free usage limit reached. Hermes safe-mode canary required explicit model; retry with explicit free provider/model returned invalid_params. No paid fallback, provider configuration change or permission relaxation performed. Codex prior live canary remains passed; OpenCode/Hermes runtime gates remain open.
- [ ] Standalone authenticated MCP client, real agent-driven corrective task submission and server-side receipt/fencing provenance remain unverified. Existing connector provides live read-only observations, not independently authenticated standalone transport. S08/S09/S13/S14 still open at their full acceptance scope.
**Decision:** Maintain bounded proposals and current Fleet scheduling/authorization; no autonomous production mutation, no hardware or deployment promotion. Continue in a separate authenticated test context when a scoped transport grant and working provider are available.
