# Decisions log

Dates are Australia/Brisbane. "Owner" is fR33k StYliN. Entries are REPORTED from the owner's instructions unless an ID or commit is given. Where a precise date was not recorded, the entry says so.

| Date | Decision or approval | Detail |
|---|---|---|
| Standing (date not recorded) | Operating loop and report format | OBSERVE -> VERIFY -> RECONCILE -> IMPROVE -> TEST -> RECORD; STATUS / DONE / RUNNING / BLOCKED / NEXT / EVIDENCE; Australian English. Default authority OBSERVE. |
| Standing (date not recorded) | Website, content and pilot rules | Preview only for websites; no CrewWorks, no A$2,500, no unverified customer or production claims, no AI Forge promotion; Discovery Sprint A$4,500 ex GST; ops pilot A$9,500 only after a completed sprint; shadow mode only; `SMTP_PASS` only as a Vercel env var. |
| 2026-11-22 | GitHub is the system of record; prefer one monorepo | Sensitive infrastructure and credentials stay out of public repos. The `fr3kd3v/fr3k` monorepo did not exist; closest platform repo is `fR3kdev/fR3k`. |
| 2026-11-22 | CI fallback rule | When hosted runners are unavailable use a free or self-hosted runner or a local reproduction. Local validate suites passed on `fR3kdev/fR3k` `main` `f983a58` and PR #8 `3f39ca8`. |
| 2026-11-22 | Waifu Fusion handed over with rules | `feature/*` or `wip/*` only, no force-push, no discarded work, never bypass permission prompts, adults-only assets, private model assets off the VPS. |
| 2026-11-22 | AI-native Android started; priority order | Scope the no-root tier on the REDMAGIC 11S Pro first; EXP-2026-002 attestation experiment second. No root, no custom ROM. |
| 2026-11-22 | Three P0.0 approvals | (1) Hexagon SDK licence accepted, owner completes the Qualcomm sign-in himself; (2) isolated test profile may be created on the REDMAGIC; all P0 and EXP work only inside it; (3) only the P0.0 toolchain-check binary may be pushed to the device. |
| 2026-11-22 | Geode job protected | Do not kill or modify Fleet Geode pack job `77f1f3a1...`; keep test profile and temp directory clear of Geode files; flag the owner when it finishes or errors. |
| 2026-11-22 | P0.0 toolchain gate passed | Fleet job `e83cc8a824c641348342ce87ce3aa6f8`, exit 0, test profile user 10 created. |
| 2026-11-23 | Divine Arsenal: finish and package | Complete gallery integration, package for PC and Android, propose free tiers and pricing aligned with Fleet. Critical logic stays on the server. |
| 2026-11-23 | Divine Arsenal Android distribution | Direct install, no Play Store, Stripe in test mode; owner build has no plan limits or device caps. |
| 2026-11-23 | Fleet release preparation | Stripe in test mode until the owner approves live keys; 1 machine always free; paid plans start at 3 machines and rise with more machines; owner asked for proposed prices. |
| 2026-11-23 | Thin-client architecture | Critical code (licensing, entitlements, pricing, billing, core logic) runs only on the owner's servers, Contabo VPS as intended home. |
| 2026-11-23 | Divine Arsenal on the phone | Termux server on the REDMAGIC 11S Pro for offline use, media copied onto the phone; on-device image generation later. |
| 2026-11-24 | Divine Arsenal "done" definition | Real app integration working, not merely the server running. |
| 2026-11-24 | Creative OS started | Store plan files as versioned markdown in one place; issues CREATIVE-001 to 008; start the CREATIVE-001 inventory; no full code yet. |
| 2026-11-24 to 25 (exact time not recorded) | fleet-mcp #431 push approved | Owner replied "Yes" to the push and "Maybe from omarchy" for the route; pushed via Omarchy `gh`. PR left open, not merged. |
| 2026-11-25 | Overlay plus waifu pipeline plan | Combine overlay videos with the 3D waifu pipeline; proof first; verified facts separate from proposals. Owner asked for it as a prompt for his dev ("Just turn this into a prompt for my dev"). |
| 2026-11-27 | fleet-mcp rebase offered | Offered to rebase #234 to #236 on Omarchy and run tests; waiting for the owner's go. |
| 2026-11-28 | This knowledge record | Owner: "Save all relevant and helpful info to GitHub". Written as a draft PR on `fr3k-research-control`; nothing merged. |

## Approvals that do not exist (do not infer)
No approval has been given to: merge any fleet-mcp PR; rebase #234 to #236; deploy any website to production; use live Stripe keys; root any device; run the on-device media benchmark.
