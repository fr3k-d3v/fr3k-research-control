# Infrastructure

Generic roles only. No addresses, hostnames, tailnet names or credentials belong here.
Last verified 28 Nov 2026 (Brisbane): Fleet device list and GitHub reads.

## Machines and roles
| Role | What it is | Notes |
|---|---|---|
| **Omarchy** | Primary Linux workstation, NVIDIA RTX 3060 (12 GB) | Builds, Android/Gradle work, local inference, wireless-debugging bridge to phones. Fleet agent online on 28 Nov 2026 (VERIFIED). The only working git push route. Gradle needs JDK 21 and a `TMPDIR` away from `/tmp` (REPORTED, 22 Nov). Parrot is retired. |
| **REDMAGIC 11S Pro** | Owner handset, Snapdragon 8 Elite Gen 5 Leading Version | Primary AI-native Android target (isolated test profile only). Owner device for Divine Arsenal (Termux server on the main profile). Geode pack work shares its storage. |
| **OnePlus 7 Pro GM1913** (Android 12) | Primary Android test device for Waifu Fusion | Tested over wireless adb from Omarchy. Fleet agent showed offline on 28 Nov 2026 (VERIFIED); do not assume it is connected. GitHub 2FA screen on it is to be left alone. |
| **Contabo VPS** | Gateway/server host | Fleet gateway (local backend, online). Intended home for critical server-side code (licence, entitlements, billing, job logic). Where `fleet-mcp approve` is typed. Intended host for self-hosted Actions runners. |
| **Vercel** | Website previews and env vars | `fr3k.dev` is owned by the older `fr3kchy` GitHub account. Previews only; `SMTP_PASS` lives only as a Vercel env var. |
| **GitHub** | System of record | Connector account `fr3k-d3v` (write access to org `fR3kdev`). Older account `fr3kchy` also exists on Omarchy `gh`. |

Other Fleet devices exist in the registry and were **offline** on 28 Nov 2026 (VERIFIED): a Chromebook, an X1 laptop, a POS Android device, a second OnePlus 7, a Reachy robot node, a rehearsal node, a spare Android node and an embedded watch (T-Watch Ultra, dispatch disabled). Treat all as unavailable until `fleet_devices_health` says otherwise.

## Git and push routes
| Route | Can do | Cannot do |
|---|---|---|
| **Omarchy `gh` / `git` (HTTPS, `fr3k-d3v`)** | Clone, branch, commit, push, open PRs, read everything | Nothing known; this is the **only push route** |
| Agent box (Grok Bot) | Read files, run scripts | No git credentials; cannot push |
| `cursor-github` connector | Read, comment, `get_job` | Cannot push |
| `user-GitHub-xai` connector | Public reads | Returns 404 on private repos |

Fleet mechanics: files go to a node with `fleet_files_write` (text, or base64 in chunks for large content); commands run with `fleet_command_execute`. A command that is held for approval returns an approval ID; the owner types `fleet-mcp approve <id>` on Contabo within 15 minutes.

## CI: hosted Actions billing lock
- **Symptom (VERIFIED 28 Nov 2026):** the latest hosted runs in `fr3k-fleet-mcp` (27 Nov, 11:55 Brisbane), `fr3k-waifu-studio` and `android-overlay-pipeline` (25 Nov) failed with **zero steps and `runner_id` 0**. That is infrastructure, not test failure. Earlier (22 Nov) the same pattern was traced to a billing lock on the `fR3kdev/fR3k` account, failing since 16 Oct 2026.
- **New evidence, needs follow-up:** on 27 Nov 2026 (19:52 and 19:53 Brisbane) two hosted runs of `SpecOps offline checks` on `fr3k-research-control` `master` **succeeded** with real runners (3 jobs, 7 steps each, VERIFIED). So the lock may be lifted, at least for that repo/account, or it is per-account. It is **UNVERIFIED** that re-running the red fleet-mcp checks would now pass.
- **Fallback rule:** use a free or self-hosted runner, or a local reproduction. fleet-mcp PRs #426 to #429 (I-007) already carry a free pinned-source CI approach through an existing Fleet runner; they are open and unmerged.
- Local test evidence is the interim proof: fleet-mcp #431 passed 738 tests plus 77 subtests locally on Omarchy (REPORTED, 24 Nov).

## Known limitations
- Fleet tools that sound read-only can queue jobs; use `fleet_devices_list`, `fleet_devices_health`, `fleet_jobs_*` for strict OBSERVE.
- Termux phone servers and Fleet agents on phones go offline; never assume a device is healthy from a registry entry.
- The `/tmp` on Omarchy has been full before; set `TMPDIR` for builds.
- The Hexagon SDK and Qualcomm libraries sit behind a Qualcomm login; `libQnnHtp*` in the vendor partition is unreadable to the shell.
- Default branch names differ: `master` for `fr3k-research-control`, `fr3k-fleet-mcp` and `fr3k-hud`; `main` for `fr3k-operations`, `fr3kcraft`, `divine-arsenal` and the Waifu repos (VERIFIED 28 Nov).

## Repository map (VERIFIED visibility on 28 Nov 2026)
| Repo | Visibility | Default branch |
|---|---|---|
| fr3k-research-control | private | master |
| fr3k-fleet-mcp | private | master |
| fr3k-waifu-studio, android-overlay-pipeline, fr3k-waifu-vault, redmagic-11s-pro | private | main |
| fr3k-operations, fr3kcraft, divine-arsenal | public | main |
| fr3k-hud | public | master |
