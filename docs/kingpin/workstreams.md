# Workstreams

State as at 28 Nov 2026 (Brisbane). Each section: state, key refs, evidence, next step. VERIFIED / REPORTED / UNVERIFIED as defined in the README.

## 1. Fleet MCP (`fr3k-d3v/fr3k-fleet-mcp`, private, default `master`)
**State (VERIFIED 28 Nov):** four PRs of interest, all open, none merged. Standing instruction: do not merge anything.

| PR | Branch | Head | Mergeable | Checks | Next |
|---|---|---|---|---|---|
| [#431](https://github.com/fr3k-d3v/fr3k-fleet-mcp/pull/431) bounded parallel agent jobs and verified binary transfers | `fix/omarchy-workers-binary-transfer-20261124` | `1fb7cd75` | mergeable (UNSTABLE) | 7 checks red; zero-step jobs | Only candidate for the owner once CI runs on a working runner; owner approves any merge |
| [#234](https://github.com/fr3k-d3v/fr3k-fleet-mcp/pull/234) F-005 recursive root deletion options | `fix/f005-root-delete-options-20261029-fr3x` | `2d2be0f5` | conflicting (DIRTY) | 4 pytest red | Rebase plus reconcile, awaiting owner go |
| [#235](https://github.com/fr3k-d3v/fr3k-fleet-mcp/pull/235) F-005 privilege launchers | `fix/f005-privileged-launchers-20261029-chatgpt-a` | `d78cd872` | conflicting (DIRTY) | 4 pytest red | As above |
| [#236](https://github.com/fr3k-d3v/fr3k-fleet-mcp/pull/236) F-012 page-fault interval preflight | `feat/f012-linux-pagefault-interval-20261029-fleet11` | `c36d088d` | conflicting (DIRTY) | 4 pytest red | As above |

**Evidence:**
- #431 base `master` was `7ab7d61` when cut; 738 tests plus 77 subtests passed locally on Omarchy (REPORTED, 24 Nov). CI failed 24 Nov ~14:22 Brisbane; job 138215579409 (py3.11, run 45325983334) had no steps and `runner_id` 0, i.e. infrastructure (REPORTED; the latest 27 Nov fleet-mcp run shows the same pattern, VERIFIED).
- #431 push was approved by the owner in chat ("Yes", then "Maybe from omarchy") and made via Omarchy `gh`.
- The red "request changes" automated reviews on #431 and #234 to #236 are inferred to come from the zero-step runs; the annotation text could not be read (UNVERIFIED).
- Other open PRs seen on 28 Nov: #433 (draft, E-005/I-002 scoped embedded MCP worker adapters, branch `feat/432-embedded-mcp-fleet-20261127`; its CI also zero-step), #426 to #429 (I-007 free pinned-source CI), and about 25 older drafts and reviews (list was capped at 30; total not counted).

**Next:** after the owner's go, rebase #234 to #236 on Omarchy (rewrites those branches), run their tests there, and report; never merge. Consider re-running #431 checks to see whether hosted CI now works (needs the owner's go as it changes PR state).

## 2. Divine Arsenal (`fr3k-d3v/divine-arsenal`, public, `main`)
**Tracked as FKKD-1 (for-review, REPORTED).** Phone setup for the owner build.
- Goal (23-24 Nov): server runs in Termux on the REDMAGIC 11S Pro (app on loopback port 8780) so it works offline with no Omarchy or network, with animation media copied onto the phone. "Done" requires real app integration working, not just the server process running. On-device image-generation tests come only after that.
- Android build is direct-install (no Play Store) with Stripe in test mode, same as PC. Owner build has no plan limits or device caps.
- Free tiers and pricing are to be proposed, aligned with Fleet: 1 machine free, paid plans from 3 machines (REPORTED, 23 Nov).
- **Open PR:** [#8](https://github.com/fr3k-d3v/divine-arsenal/pull/8) (draft, ten-style animation workflow doc, mergeable; updated 13 Nov).
- **CI (VERIFIED):** newest runs (13 to 21 Nov) succeeded, including run on `backup/divine-arsenal-20261121` (head `1318ad53`).
- **State of the device job:** an earlier Fleet job for the phone setup (`105e639a...`) probably expired its approval TTL (REPORTED); resubmit when the owner asks. Unverified whether the phone is currently reachable.
- **Constraints:** see [operating-rules.md](operating-rules.md).

## 3. Waifu Fusion and the overlay pipeline
**Tracked as FKKD-4 (plan and dev prompt delivered; for-review, REPORTED).**
- Repos (private): `fr3k-waifu-studio`, `android-overlay-pipeline`, `fr3k-waifu-vault` (284-part manifest `catalog/actual-waifu-fusion-284-parts.csv`). One APK, `dev.fr3k.waifufusion`. Rules: `feature/*` or `wip/*` only, see operating rules.
- **Overlay format `packed-alpha-v1`:** 2920x624 H.264 at 24 fps; colour on the left half, alpha on the right half. Played by `PackedView` (ExoPlayer). `FilamentCharacterView` (Filament 1.68.2) renders GLB characters. `CreatureVoiceCore` voice phases drive only the Filament view; **there is no lip-sync code** (REPORTED, 25 Nov).
- The existing overlay videos are animal and monster creature clips, not waifus.
- **Owner direction (25 Nov):** combine overlay videos with the 3D waifu pipeline using Waifu Studio, the overlays and the YouTube transcript knowledge base; verified facts separate from proposals.
- **Dev prompt stages (REPORTED; last note truncated):**
  1. Proof first: render a Nova idle clip to `packed-alpha-v1` and play it through the **unchanged** `PackedView`.
  2. Per-character voice-phase map for both renderers (server-sourced).
  3. Crossfade between both renderers.
  4. Lip-sync via Android system TTS, **without vendoring Piper** (GPL).
  5. Optional: Filament external stream texture (rest of the note not preserved).
- **Branches carrying the proof work (VERIFIED 28 Nov):**
  - `fr3k-waifu-studio`: `feature/studio-linked-packed-alpha-proof-20261125` at `4414782b` (local deterministic GLB idle proof renderer) and `feature/asset-rights-reconciliation-20261125` at `ecf33549` (reconcile redistribution claims and guards).
  - `android-overlay-pipeline`: `feature/studio-linked-packed-alpha-proof-20261125` at `8fb8309a` (verify local packed-alpha GLB idle proof).
  - Other live branches: `feature/native-waifu-fusion-20261122`, `feature/oneplus7pro-waifu-fusion-20261122`, `feature/oneplus7pro-library-ux-20261122`.
- **CI:** latest runs on these branches failed with zero steps (billing-lock pattern, VERIFIED); proof of the renders is therefore local only. On-device playback on the OnePlus 7 Pro is UNVERIFIED (device offline on 28 Nov).
- **Open PRs:** studio #1 and #3 (drafts); overlay-pipeline #9, #10, #11, #12, #14, #15, #16 (drafts, 12 to 21 Nov; only the newest 8 PRs were listed, so older ones may exist). Studio #2 and overlay-pipeline #17 are merged.
- **Next:** the dev works stage 1 on a `feature/*` branch; no device test without the owner's approval of the Fleet job. Job `fc6d7620` for Waifu Fusion is listed in the backlog (REPORTED; state unverified).

## 4. AI-native Android (`fr3k-d3v/redmagic-11s-pro`, private, `main`)
- Started 22 Nov from the BLACKSITE deep dive (experiments EXP-2026-001 to 007). Scope: no-root tier on the REDMAGIC 11S Pro using llama.cpp (OpenCL/Adreno, experimental Hexagon), GenieX as baseline.
- **Estimate (REPORTED, 22 Nov):** P0 to P3 about 54 engineer-days (44 to 75); P0 to P4 about 70. Phases: P0.0 access/licence/toolchain gate (2 days), P0 bake-off (14), P1 NPU owner with MCP and AppFunctions (12), P2 accessibility agent (18), P3 EXP-2026-002 (10), P4 privileged service (16). EXP-2026-001 bake-off covers llama.cpp CPU/OpenCL/Hexagon, GenieX, LiteRT-LM and MNN (about 18 days, 14 to 24). Commercial kill gate: if no NPU path gives correct output within 30 days, the porting offer is dropped.
- **P0.0 toolchain gate passed on 22 Nov (VERIFIED by job):** Fleet job `e83cc8a824c641348342ce87ce3aa6f8`, exit 0. Created isolated profile user 10 (`FR3K-P00-test`). Toolchain-check binary sha256 `fdea1cdc612434678a7a2dedbddc86553d07ac30b61ab2a664a98a7f7bad803c`. OpenCL 3.0 on Adreno 840; fastrpc cdsp/nsp nodes present; `libQnnHtp*` unreadable to the shell (EACCES).
- **Licence findings (22 Nov):** Geode is AGPL-3.0, not to be vendored; calling other apps' AppFunctions needs privileged `EXECUTE_APP_FUNCTIONS` so a sideloaded agent can only provide functions; Hexagon SDK is behind a Qualcomm login.
- **Branches seen (VERIFIED 28 Nov):** `feature/p0-0-toolchain-gate`, `experiment/mobile-ai-termux-mcp-20261122`, `audit/engineering-2026-11-22`, `work/android-fielddesk-20261123` (its CI also zero-step).
- **Blocker:** the owner must complete the Qualcomm sign-in himself; queue the prompt and flag it.
- **Geode:** Fleet job `77f1f3a1...` (Geode pack) must not be killed or modified; Geode's native work is left alone. Its state on 28 Nov is UNVERIFIED.

## 5. Creative OS (FKKD-3, for-review; BLOCKED, REPORTED)
- Started 24 Nov from `FR3K-CREATIVE-OS-OPPORTUNITY-PLAN-2026-11-24.md` plus a schema draft and a P1 disposition checklist.
- Ask: store them as versioned markdown in one coherent place; create issues CREATIVE-001 to 008 linked to the plan; start the CREATIVE-001 inventory (existing FR3K interfaces the character vertical slice can reuse: workspace, Android overlay, SENTIENCE, Fleet, voice). No parallel orchestrator and no full code yet.
- **Blocked:** the plan, schema draft and P1 checklist have not been received. The branch `docs/creative-os-20261124` does **not** exist on `fr3k-research-control` (VERIFIED 28 Nov: only `master` and `agent/chatgpt/ctx-64k-manager`). No Creative OS issues were created.
- **Next once files arrive:** branch `docs/creative-os-20261124` from `master`, files under `research/creative-os/`, push via Omarchy, draft PR; then issues CREATIVE-001 to 008; then the inventory. This kingpin record deliberately leaves that path alone.

## 6. Websites and fr3k.dev preview
- Rule: preview only; owner approves each production deploy himself. SMTP only as a Vercel env var. Pilot-offer wording rules are in operating rules.
- Open items (REPORTED, not re-verified): pricing, GST treatment, Stripe test keys, `SMTP_PASS` provisioning, the `fr3k.dev` preview. Current preview URLs and deploy state were not checked in this pass (UNVERIFIED).
- `fr3k-d3v/fr3k-operations` ([#15](https://github.com/fr3k-d3v/fr3k-operations/pull/15), BLACKSITE research catalogue templates, mergeable, updated 22 Nov) awaits a read-only review; merging needs the owner's approval. `fr3k-operations` and `fr3kcraft` have no workflow runs (VERIFIED).

## 7. Other public work seen this week (VERIFIED where linked)
- `fr3kcraft`: free multiplayer guide update ([e956fe0c](https://github.com/fr3k-d3v/fr3kcraft/commit/e956fe0cf974d72f3a08f154a45b59bd6259210c)); open draft PR #1 (Joy Luanti handoff).
- `fr3k-hud`: v0.4.16 prerelease; FR3K ONE contract docs merged in #3; open draft #2 is conflicting.
- `fr3k-research-control`: SpecOps (read-only Fleet receipt observation and bounded convergence proposals; not a scheduler or release authority), embedded-hardware and dynamic-UI research notes. Hosted CI for SpecOps passed on 27 Nov (see infrastructure).
