# FR3K research: dynamic UI, embedded agents and fleet convergence

Date: 2026-11-27. Status: discovery and README audit, NOT deployment or hardware acceptance.
Related: fr3k-d3v/fr3k-fleet-mcp#432. Scope: improve the shared fleet/UI architecture, not replace the authoritative orchestrator.

## Search method and evidence
GitHub repository searches explicitly used stars:0 and stars:0..10 for A2UI/LVGL, ESP32 A2UI, Cardputer Lua, Tab5 OS, K230 LVGL, Reticulum ESP32 and ESP32 agent MCP. The connector returns names but not numeric star counts or creation/push dates; membership in the returned filter is the evidence, not a separately retrieved exact count. Public search supplemented the connector. README blob SHA values below identify the inspected document (not a source commit). No assertion of exhaustive coverage or last-month creation dates. Pin source commits and inspect LICENSE before adoption.

## Priority 0: architecture-changing discoveries

| Repository | Evidence | Proposed adoption |
|---|---|---|
| [faluciano/a2ui-lvgl](https://github.com/faluciano/a2ui-lvgl) | Low-star filter; README blob 0701cf0cb4da9f585fe81ca9a7e5e891cc9f82e3. Author reports v0.1.0, Apache-2.0, A2UI v1.0, LVGL 9.6, 18 components, ESP32-P4 hardware run, builds for ESP32/S3/C3/P4, 672 conformance passes and one exception. | Evaluate as primary native renderer before writing our own. Inspect RAM budgets, event routing, license and upstream exceptions; test on Tab5 and K10. |
| [jaklys/Lvgl-mcp-esp32](https://github.com/jaklys/Lvgl-mcp-esp32) | Public README documents MIT, headless JSON/C render, screenshots, object tree, clipping/contrast/font/heap diagnostics and interaction/diff tools. C execution is explicitly unsandboxed. | Omarchy preview pipeline: validate UI, render each board profile, inspect, repair and rerender. JSON-only by default; isolate C builds in disposable containers without credentials. |
| [stramanu/esp32sim-mcp](https://github.com/stramanu/esp32sim-mcp) | Low-star filter; README blob 443d92824f4beef087a89371c3e5fce6c96a770b. MIT claimed, emulated ESP32/S3/C3/C6 boot, UART, GPIO, virtual Wi-Fi, touch/screenshots and assertions. | Preflight firmware in isolated emulation before hardware; not evidence of physical peripherals or P4 support. |
| [huichen/esp32-agent](https://github.com/huichen/esp32-agent) | Low-star filter; README blob 51381da9eb0595a547b724a1a1fa26614adfeb50. Author describes live JSON manifests, I2C/1-Wire probe, MCP endpoint, scheduling, skills, transcripts, virtual board. | Reuse discovery and manifest ideas, not an independent privileged agent. Fleet owns leases, authority, and scheduling. Audit TLS, secret handling and tool validation. |

## Small repository candidates
- [squirrelsoft-dev/a2ui-embedded](https://github.com/squirrelsoft-dev/a2ui-embedded) — zero-star search; README blob 8662e080409a81e683add326c95612877ca48f49. Explicitly concept/pre-development. Driver shim, LVGL and AG-UI SSE, hybrid local/remote actions; use as design comparison, not code readiness.
- [lilieming/llm-a2ui-lvgl](https://github.com/lilieming/llm-a2ui-lvgl) — low-star; README blob fa02eb4249354d53eeb472092b957efa322bca75. C, cJSON, A2UI v0.9, data binding, orphan cleanup, LVGL events. Alternative constrained renderer design; protocol version differs.
- [matia6170/cardputer-lua-interpreter](https://github.com/matia6170/cardputer-lua-interpreter) — zero-star; README blob b57d3b329f4eb2be5295e56407448b0b14fc0634. Original Cardputer Lua 5.4, SD scripts, keyboard/serial REPL, interruption, author reports ~17 KB free heap after stdlib. Full stdlib unsuitable for untrusted remote execution without restrictions.
- [TeamHarrisCali/PocketLua](https://github.com/TeamHarrisCali/PocketLua) — zero-star; README blob 220aa227f764e45417c0890a3ee79b7f767c9937. ADV live editable Lua apps, catalog, hashes and rollback. Original Cardputer compatibility unknown; use packaging and recovery concepts, require signed manifests in addition to hashes.
- [moisesfilho/tab5-os](https://github.com/moisesfilho/tab5-os) — low-star filter; public README describes .tab5pkg packages, app discovery, permissions and screenshots. Inspect loader security, ABI and package isolation.
- [moisesfilho/tab5-app-terminal](https://github.com/moisesfilho/tab5-app-terminal) — zero-star; README blob 9a28f2de0e98c99ca29e03d73ffc6debbe260471. Packaged terminal with small command set, not evidence of full Linux shell.
- [liamcottle/microReticulum](https://github.com/liamcottle/microReticulum) — low-star; README blob 7814891cb030111eb6a1fa64806c3491054c6c8b. C++ MCU stack; upstream roadmap still includes constrained memory, links/resources/channels and board targets. Do not treat as production mesh.
- [contextablemark/esp32-agui](https://github.com/contextablemark/esp32-agui) — public indexed plan, direct fetch blocked. Candidate only.
- [00000000o62/k230-llm-chat](https://github.com/00000000o62/k230-llm-chat) — low-star search result, README fetch returned 404. UNKNOWN, no recommendation.

## Established complementary references
- [A2UI upstream](https://github.com/a2ui-project/a2ui) — protocol, native Android/Compose, Flutter/web renderers. Use shared catalog and data model, with constrained board profiles.
- [CanMV K230 AI guide](https://www.kendryte.com/k230_canmv/en/main/ai_dev_doc.html) and [CanMV releases](https://github.com/kendryte/canmv_k230/releases) — vendor documents LVGL over AI inference and serialized KPU access; use separate native K230 worker.
- [RisalDash](https://github.com/ziyarago/RisalDash) — public README documents offline AP/captive portal, WebSocket, MCP and dashboard widgets. Candidate for browser-based fallback, not native screen renderer.
- [flxos](https://github.com/flxos-labs/flxos) — public README describes YAML hardware profiles, event bus, storage and ESP32 family support. Compare hardware abstraction, do not introduce second OS without need.
- [ForgeUI-P4](https://github.com/RTechAI/ForgeUI-P4) — P4 LVGL/ESP-Hosted baseline; [Tab5 dashboard](https://github.com/Ninune-wa/TAB5-WallDashboard) — actual Tab5 P4/C6 reference.
- [ESP32-UI](https://woodleyj.github.io/projects/esp32-ui) — project page describes MQTT-delivered LVGL widget trees and fragmentation constraints.
- [loadout-tab5](https://github.com/0day1day/loadout-tab5) — indexed mirror describes OTA rollback and hardware utilities; direct repository verification outstanding.

## Proposed implementation delta
1. Fleet publishes versioned capability profiles: screen geometry, input, supported widget/catalog versions, free memory, render limits, hardware actions and transport.
2. Model generates bounded A2UI surfaces; gateway validates against capability profile and policy. Use A2UI v1.0 renderer candidate on P4/S3; small Cardputer profiles can use text/menu renderer, and K230 uses CanMV overlay. Android and Linux use native/web renderers.
3. Preview every target profile on Omarchy with LVGL MCP. Render screenshots, verify layout and simulate input. Keep raw evidence and distinction SIMULATION vs VERIFIED HARDWARE.
4. Publish immutable signed app/surface manifests with hash, revision, declared capabilities, quotas and previous-known-good reference. Device stages, validates, acknowledges and activates atomically; retain offline snapshot.
5. UI events are data, not commands. Gateway maps allowed action IDs to scoped Fleet jobs, enforces authority, fencing, expiry, deduplication and audit. No arbitrary code in UI JSON; Lua skills separate with explicit permission, instruction/time/memory quotas and restricted bindings.
6. Data model patches and event receipts use monotonic revisions; offline LoRa transports only compact commands/telemetry or cached-template patches, not full images or arbitrary code. Camera/video use separate authenticated media channel.
7. Test: host protocol fixtures, renderer screenshots, interaction/diff assertions, emulated firmware boot, malicious payloads, low-memory, disconnect/reconnect, battery and rollback; then board-by-board physical acceptance. Record device model, firmware hash, raw photo/screenshot, actual input/output and measured latency/memory. Never claim a hardware pass from emulation.

## Next source audit
Inspect pinned commits, license files, build lockfiles, native board configuration, protocol conformance exception, memory measurement, transport auth, input lifecycle, package recovery and test reproducibility. Evaluate with isolated Codex/Hermes workspaces; no production deployment or flashing authorized by this research note.
