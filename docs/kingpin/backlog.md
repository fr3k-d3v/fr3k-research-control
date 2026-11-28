# Backlog

Open items as at 28 Nov 2026 (Brisbane). Authority: OBSERVE (read only), AUTO (reversible, branch plus PR), APPROVAL (owner's own words needed), PHYSICAL (hardware).

| # | Item | Authority | Blocker / dependency | Next action |
|---|---|---|---|---|
| 1 | Rebase and reconcile fleet-mcp #234, #235, #236 on Omarchy, run tests, report | APPROVAL (rewrites branches) | Owner's go (offered 27 Nov, not yet given) | On go: rebase on current `master`, run tests, report results; no merge |
| 2 | fleet-mcp #431: get a CI result | OBSERVE to check; APPROVAL to re-run or merge | Hosted CI may be unlocked (SpecOps runs passed 27 Nov) but unverified for fleet-mcp; free-runner path in #426-#429 is unmerged | Ask owner whether to re-run the checks; merge remains the owner's decision |
| 3 | Free-runner CI for `fr3k-operations` and `fr3kcraft` (0 workflow runs each) | AUTO (branch plus PR); APPROVAL to merge | Choice of self-hosted runner on Contabo or Omarchy | Draft a basic CI workflow on a free or self-hosted runner, open a PR |
| 4 | Read-only review of `fr3k-operations#15` | OBSERVE; APPROVAL to merge | None for the review | Review and report; do not merge |
| 5 | Stripe test keys, GST treatment and pricing proposal (Fleet, Divine Arsenal; pilot offer wording) | APPROVAL | Owner supplies or approves keys (test mode only until he approves live keys); pricing and GST need his sign-off | Prepare proposal; keep keys out of chat, store as env vars only |
| 6 | `SMTP_PASS` as a Vercel env var | APPROVAL | Owner must provision it; never as plain chat | Remind owner; never print it |
| 7 | `fr3k.dev` preview | AUTO for preview; APPROVAL for production | Owner approves each item before any production deploy | Preview only; state of current preview UNVERIFIED |
| 8 | Qualcomm Hexagon SDK sign-in | PHYSICAL / owner-only | Owner completes the interactive sign-in himself | Queue the prompt and flag it; do not bypass or fake acceptance |
| 9 | Divine Arsenal phone setup (FKKD-1) | PHYSICAL (owner-approved Fleet job) | Earlier job `105e639a...` probably expired; phone reachability unverified | Resubmit when the owner asks; one queued device job at most |
| 10 | Waifu Fusion Fleet job `fc6d7620...` | PHYSICAL | State unverified in this pass | Check with `fleet_jobs_*` (read only); do not touch jobs `bd7aca4a` or the Geode job `77f1f3a1...` |
| 11 | Overlay stage 1: Nova idle clip as `packed-alpha-v1` through unchanged `PackedView` (FKKD-4) | AUTO on `feature/*` | Local proof exists on `feature/studio-linked-packed-alpha-proof-20261125`; on-device playback needs an approved device job | Dev continues on the feature branch; hardware verification is separate from the local render |
| 12 | Creative OS (FKKD-3): plan files, issues CREATIVE-001 to 008, CREATIVE-001 inventory | AUTO once files arrive | Plan, schema draft and P1 checklist not yet received | Branch `docs/creative-os-20261124`, files under `research/creative-os/`, draft PR via Omarchy |
| 13 | GitHub billing lock on hosted Actions | APPROVAL (owner's account) | Owner action in GitHub billing; evidence is mixed (see infrastructure) | Owner to check billing; do not assume resolved |
| 14 | Four open PRs not yet reviewed from the backlog search | OBSERVE | None | `fr3kcraft#1` (draft), `fr3k-hud#2` (draft, conflicting), `divine-arsenal#8` (draft), plus `fr3k-operations#15`; review read-only |
| 15 | Open issue triage: relayguard-demo 29, fr3k-operations 13, divine-arsenal 8, fr3k-research-control 7 (counts from 27 Nov, not re-counted) | OBSERVE | None | Triage when asked |
| 16 | Consolidate into one `fr3kd3v/fr3k` monorepo (or confirm `fR3kdev/fR3k` as the home) | APPROVAL | Authoritative remote not confirmed | Owner decision; until then keep this repo as the research coordination entry point |
| 17 | Housekeeping: close or update tracked task FKKD-4 (overlay plan delivered) | OBSERVE | None | Mark done once the owner confirms |

## Not approved (do not do)
Rooting any device; a custom ROM; the on-device media benchmark for Divine Arsenal; production deploys of websites; merging any fleet-mcp PR; force-pushes; killing or modifying the Geode job or other Omarchy jobs.
