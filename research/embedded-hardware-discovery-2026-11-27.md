# Embedded hardware discovery — 2026-11-27

Window: 2026-10-27 through 2026-11-27 inclusive. Prior discovery transcript archived below; dates and stars are historical reported observations, not independently refreshed in this pass. Repository contents are not hardware acceptance evidence. No firmware installed. Public upstream links only.

## Candidate inventory
Columns: upstream (https://github.com/ + owner/repo), stars, created, last push (2026), qualification from prior scan. Dash = not recorded.

| Group | Upstream | Stars | Created | Push | Notes |
|---|---|---:|---|---|---|
| Tab5 | tsuyoshi-otake/m5stack-tab5-linux | 1 | Nov 10 | Nov 25 | Native NOMMU SMP Linux, experimental |
| Tab5 | Belekos/Tab5OS | 5 | Nov 1 | Nov 11 | GUI, files, drawing, media, maps, MicroPython, ELF apps |
| Tab5 | DuanWeiye/Tab5WirelessDisplay | 0 | Nov 15 | Nov 15 | MIT; wireless PC display/audio/input |
| Tab5 | cbw29512/Tab5LASR | 0 | Nov 17 | Nov 24 | Early planning, camera pipeline not demonstrated |
| Watch | armSeb/Twatch-ultra | 0 | Nov 23 | Nov 26 | ESP-IDF 5.5, LVGL 9, NimBLE, iPhone companion, battery |
| Watch | ColinDuch/CD-OS-T-Watch_ultra | 0 | Nov 10 | Nov 19 | Watch firmware |
| Watch | Redwindmh/ReticulumWatch-v1.6.1 | 0 | Oct 30 | Oct 30 | S3 target, not Ultra; LXMF text and Codec2 short voice; no top-level license reported |
| Watch | TheExoned/Exosys-OS | 3 | Oct 28 | Oct 29 | ESP32-S3 RTOS, zero-copy/maps/A*/video/remote control claims |
| K230 | xhtfps/esp32-k230-ai | 0 | Nov 22 | Nov 23 | MIT; dual-board edge vision/robotics/voice |
| K230 | traft00/meshcore-k230 | 1 | Nov 6 | Nov 6 | LoRa messaging feasibility, not working firmware |
| K230 | Jackbinson/CanMV-K230-cloud | 0 | Nov 2 | Nov 11 | Cloud integration candidate |
| K230 | chabaihe/vehicle-model-recognition-K230D-Agent | 5 | Oct 27 | Nov 2 | ResNet-50/ReAct; 28 FPS author claim |
| Cardputer | MarsTechHAN/deepseek-harness-tui-cardputer | 9 | Nov 17 | Nov 19 | Rust tools/goals/context compaction; CM0 Zero only |
| Cardputer | thededman/HAL9000 | 4 | Nov 7 | Nov 19 | Local multi-device voice personalities |
| Cardputer | arthubhub/meshcore-cardputer | 7 | Nov 3 | Nov 22 | ADV/LoRa-1262, messaging, maps, GPS, BLE |
| Cardputer | konsumer/cardbuddy | 7 | Nov 17 | Nov 19 | Candidate |
| Cardputer | UMEBOSHIISAN/cardputer-voice | 2 | Nov 19 | Nov 20 | Voice candidate |
| Cardputer | BenjaminAddison/launcher_orbit | 6 | Oct 28 | Nov 12 | Launcher candidate |
| K10/ESP32 | vb3227/esp32-mcp | 1 | Nov 2 | Nov 2 | MIT, MCP/Lua/skills/relay/K10 adapter |
| K10 | manwjh/open-knot-agent | 0 | Nov 24 | - | Apache-2.0; placeholder, planned Dec 1 |
| ESP32 | pocket-nexus/m5stack-firmware | 8 | Nov 22 | Nov 25 | MIT, PocketJS/AOT; Tab5/StickS3/AtomS3/StopWatch |
| T-Deck | geekgarage/dualmesh | 2 | Nov 23 | Nov 26 | MIT; MeshCore and Meshtastic time share SX1262, maps/GPS/BLE/encrypted SD/OTA claims |
| T-Beam | alexandergmzx/swarm-node-firmware | 0 | Nov 25 | - | Candidate |
| Watch | Vikappa/daemonOS | 0 | Nov 25 | - | Candidate |
| T-Deck | janix12/T-Deck-FlightDeck | 0 | Nov 26 | - | Candidate |
| K230 | Intelligienic-Technology/k230_camera_sdk | 0 | Nov 13 | - | Camera SDK |
| Watch | aykutsevim/aerodeck-twatch-ultra | 0 | Nov 11 | - | Candidate |
| Watch | aquasock/TTWatch | 0 | Nov 11 | - | Candidate |
| T-Deck | digicyc/huckleberry | 0 | Nov 9 | - | MeshCore candidate |
| Tab5 | pixitha/Tab5-DualMesh | 0 | Nov 3 | - | DualMesh candidate |
| ESP32 | pocket-nexus/pocket-hub | 0 | Nov 12 | - | Embedded app management |
| LoRa | IU5HJU/VoLoRa | 0 | Nov 2 | - | Voice/LoRa candidate |

## Older, recently pushed
| Upstream | Stars | Last push |
|---|---:|---|
| Xinyuan-LilyGO/T-Display-K230 | 13 | Nov 26 |
| kendryte/k230_linux_sdk | 68 | Nov 26 |
| bmorcelli/Launcher | 2420 | Nov 26 |
| rockets-cn/unihiker-k10-skills | 8 | Nov 26 |
| Xinyuan-LilyGO/LilyGoLib | 160 | Nov 24 |
| kendryte/canmv_k230 | 128 | Nov 23 |
| laserir/MCLite | 49 | Nov 16 |

## Fresh source observations (2026-11-27)
- [HAL9000 README](https://github.com/thededman/HAL9000/blob/main/README.md): author documents v0.7.0, CoreS3 desk unit, Cardputer Zero conversation conductor, original Cardputer participant, M5StickC Plus2 text/chirps, M5Paper minutes. Local Ollama, Piper, whisper.cpp on host. CoreS3 standalone prerecorded SD audio; live generation needs host. macOS setup tested by author, Linux not yet tried. Simulator available; MIT code, third-party voice model separate. FR3K: reuse UI/personality protocol concepts; keep authoritative orchestrator external; adapt original Cardputer/watch/Tab5 separately.
- [Tab5 Linux README](https://github.com/tsuyoshi-otake/m5stack-tab5-linux/blob/main/README.md), README blob 3f4e9168d079e475f66e5ba222be5cee45b42c52: v0.7.1 early preview, Linux 7.2.11 NOMMU SMP, both P4 cores, C6 SDIO Wi-Fi, BusyBox, Dropbear SSH, MicroPython, framebuffer/touch, USB host, microSD, IMU/RTC, BLE keyboard, audio capture/playback, one-shot raw camera. Author tests on ST7121 panel only, other panels unverified; no V4L2/video, full BlueZ, normal MMU process isolation. C6 factory firmware replacement necessary for Wi-Fi; original C6 restoration untested, P4 dump alone insufficient. Secure boot/flash encryption disabled; local programs have full device access. Gate: identify board/panel, establish both-chip recovery before flashing; GPL-2.0-only with component exceptions. [Author hardware report](https://github.com/tsuyoshi-otake/m5stack-tab5-linux/blob/main/linux/tests/v0.7.1-hardware-validation-2026-11-25.md).
- [Open Knot Agent README](https://github.com/manwjh/open-knot-agent/blob/main/README.md), blob f9c3045bcebf16cf0041d88f2e9f0393414619b2: confirms placeholder and planned 2026-12-01 source release; intended K10 ESP32-S3, cloud model, non-blocking state machine, flash memory, host test suite. Apache-2.0. BLOCKED until published; no working implementation verified.
- [ESP32 MCP README](https://github.com/vb3227/esp32-mcp/blob/main/README.md), blob df64c6df9194d0ff6098eb6aff000e7006e179dd: MIT; host MCP stdio, local HTTP or authenticated outbound WSS relay; K10 specific display, RGB, sensors, mic/ASR, camera/media/voice adapter; generic ESP32/S2/S3/C3/C6/WROVER profiles. Lua 5.4.9 on MCU, JSON skills, restricted host Python, 32 driver catalog, background job IDs/mailboxes, four Lua and four K10 hardware slots sharing resources. Explicit GPIO allowlist; time/memory/instruction limits, not hostile-code isolation. NVS install distinct from host save; no boot autorun. Voice local/Groq STT + Codex, credentials host-side. One board per gateway; no public cleartext HTTP. [Drivers](https://github.com/vb3227/esp32-mcp/blob/main/docs/DEVICE_DRIVERS.md), [testing](https://github.com/vb3227/esp32-mcp/blob/main/docs/TESTING.md), [releases](https://github.com/vb3227/esp32-mcp/releases/latest). FR3K: use K10 as pilot, review pin mapping, auth, bounds and read-only probes before granting operations.

## Proposed architecture / priority
Authoritative fleet orchestrator -> inference/relay host -> wearable voice node, Tab5 command terminal, K230 edge vision nodes, Cardputer/K10 tools -> off-grid T-Deck/T-Beam communications. Proposal only, not deployed. Prior priority: ESP32 MCP, Tab5 Linux, DualMesh, HAL9000, ESP32-K230-AI, PocketJS, armSeb watch, ReticulumWatch, Tab5WirelessDisplay, Open Knot Agent. Prefer first testing ESP32 MCP and HAL simulator; hold Tab5 write pending recovery; monitor Knot release. No private inventory, credentials, hostnames, internal topology or raw device evidence recorded. All unreviewed candidate details remain prior-scan claims.
