# GPD Win Mini: Omarchy analysis and Windows/Fedora/Omarchy triple-boot plan

Research date: 2026-11-10 (Australia/Brisbane).
Status: RESEARCH AND PROPOSED CONFIGURATION. No GPD installation, partition change or hardware validation has been performed.

## Objective and scope

Preserve Windows and Fedora already installed on the GPD Win Mini's single internal SSD, and add Omarchy as a third independent operating system. Earlier discussion of a separate drive is superseded by this same-drive requirement.

Omarchy is Arch-based; it is not installed into Fedora as a desktop package set. Fedora can be used to inspect the disk and prepare installation media. The intended result is a customised FR3K handheld workstation, while retaining Windows for games/vendor software and Fedora as an independent Linux work and recovery environment.

## Evidence status

- USER-REPORTED: Windows and Fedora already occupy the same SSD.
- VERIFIED DOCUMENTATION: Current Omarchy instructions describe free-space installation alongside existing operating systems, LUKS encryption and Limine boot-menu discovery.
- OBSERVATION: The official website retrieved during this research advertised Omarchy 4.5.0. This is a retrieval-time observation, not proof of the version installed on any device.
- UNKNOWN: Exact GPD generation, CPU, RAM, SSD capacity, partition layout, filesystem types, encryption, free space, firmware, Secure Boot state and hardware compatibility.
- PROPOSAL: The configurations, storage budgets, workflow and acceptance criteria below.
- NOT VERIFIED: Triple boot, suspend, controller/gyro support, battery life, gaming performance or deployment on the GPD.

Documentation can change. Validate the chosen ISO and installed package versions before using configuration syntax.

## Assessment

Omarchy's strengths for this use are a configurable Hyprland environment, integrated developer workflows, coordinated theming, and an update/recovery workflow. Its costs are accepting the distribution's opinionated defaults, maintaining compatibility with its updates and separately validating handheld functionality.

Use Windows for existing games, vendor utilities and Windows-specific software. Keep Fedora's existing environment intact. Use Omarchy for FR3K coding, hardware tooling, remote job inspection and fleet control.

Treat the handheld as a responsive mobile workstation. Route heavy GPU processing and persistent jobs to appropriate remote workers; do not assume the handheld must reproduce every server workload.

## Installation design

1. Inventory partitions, filesystems, mount points, encryption and UEFI boot entries.
2. Back up important files, partition/boot information and recovery material. Store encryption recovery keys securely outside the repository.
3. Use existing unallocated space if available.
4. If space must be created, decide which filesystem can safely shrink. Prefer Windows Disk Management for Windows volumes. Fedora resizing depends on the actual filesystem and any encryption/LVM layers; do not prescribe generic partition commands.
5. Download and verify the selected Omarchy ISO; prepare a bootable USB.
6. Boot the installer in the appropriate UEFI mode.
7. Select **Free space install**, never the whole-disk option.
8. Review the exact partition changes before applying them. Preserve Windows, Fedora, recovery partitions and existing EFI files.
9. Install Omarchy into its own space, preferably encrypted.
10. Preserve Windows Boot Manager and Fedora's bootloader and firmware boot entries.
11. Configure a convenient boot menu, then test each independent boot path.
12. Only after baseline hardware validation, apply custom profiles incrementally.

Current documentation describes using `limine-scan` to add other installations. Discovery is not proof of a working Fedora entry. Prefer allowing Fedora to keep managing its own kernels through its own bootloader. Choose EFI partition handling only after inspecting the real layout; do not assume available ESP capacity or format an existing ESP.

A clearly visible boot menu with enough time to select an OS is preferable to direct boot on a triple-boot handheld. Keep firmware boot selection as a fallback.

## Space budget

These are planning recommendations, not official minimums:

| Allocation | Intended use |
|---|---|
| 80–120 GB | Evaluation, browser, SSH and light development |
| 150–250 GB | Comfortable development workstation |
| 300 GB or more | Large containers, Android SDKs, local models and games |

A provisional target is around 200 GB if existing installations can spare it. Budget for package caches, snapshots, SDKs, container images, models and optional hibernation.

Keep Fedora and Omarchy home directories independent. Share selected project/data directories deliberately rather than sharing an entire home directory and mixing incompatible settings.

## Secure Boot and BitLocker

Omarchy does not support Secure Boot by default in the installation material consulted. Inspect the current configuration and Windows recovery arrangements before firmware changes. Disabling Secure Boot may affect Windows software requiring it. Do not clear the TPM.

The Omarchy installer documentation asks users to disable BitLocker. Its explanation that BitLocker necessarily encrypts the entire physical disk is inaccurate: Microsoft documents volume encryption. Distinguish an installer restriction from BitLocker's technical capabilities. Check the chosen installer release and actual Windows encryption state before proceeding. Never commit recovery keys.

## Proposed FR3K GPD configuration

| Area | Proposed setup |
|---|---|
| Handheld desktop | Readable text, large controls, minimal gaps and one primary window per workspace |
| Docked desktop | External-monitor scaling and denser multiwindow layouts |
| Display | Trial approximately 150–175% scaling, tuned to the actual panel and eyesight |
| Refresh rate | Separate battery/AC preferences, using modes the panel actually exposes |
| Input | Keyboard shortcuts, touchpad tuning and correct touchscreen mapping |
| Touch access | Optional on-screen keyboard and usable menu targets |
| Controller | Explicit desktop and application mappings after baseline input tests |
| Power | Quiet battery, balanced work and measured AC performance profiles |
| Fleet console | Device/job views with evidence timestamps and explicit stale/unknown states |
| Development | Git, editor, isolated language environments and project-specific dependencies |
| Android | ADB, APK inspection and remote build/test access |
| Hardware | Serial tooling and scoped permissions for connected development boards |
| Appearance | FR3K palette, high contrast, restrained effects and useful instrumentation |
| Recovery | Independent boot options, system snapshots, config/data backups and rescue media |

Suggested workspaces: Fleet, Code, Browser and Hardware. Provide quick controls for brightness, audio, Wi-Fi, power profile and keyboard. Desktop control mappings must not accidentally trigger privileged fleet actions.

## Configuration and version compatibility

The current documentation uses Lua-based Hyprland configuration and Omarchy shell configuration. Older guides use different paths and syntax. Inspect the installed version before implementing.

Current documented user files include:

- `~/.config/hypr/hyprland.lua`: main configuration and overrides.
- `~/.config/hypr/bindings.lua`: bindings.
- `~/.config/hypr/monitors.lua`: display rules.
- `~/.config/hypr/input.lua`: input.
- `~/.config/hypr/looknfeel.lua`: gaps, borders and animation.
- `~/.config/hypr/autostart.lua`: session applications.
- `~/.config/omarchy/shell.json`: shell layout and associated settings.
- `~/.config/foot/foot.ini`: terminal settings.
- `~/.config/omarchy/themes`: custom themes.

Keep distribution files under `/usr/share/omarchy` unchanged; use supported user overrides. Current theme documentation uses `colors.toml` for a coordinated palette across shell, terminal and editors.

Monitor controls cover scaling, refresh rate and rotation. Hyprland supports per-device input settings and touch transforms. Identify the real panel and input device names before writing rules.

## Handheld hardware support

Handheld Daemon explicitly lists the GPD Win Mini. Its documentation includes a 2025-model WinControls limitation and warns that generic installations can break with kernel/Python changes. Supported-device listings are leads, not proof that every function works on this Omarchy installation.

Test built-in input first. Add HHD or other device-specific components only for demonstrated needs. Avoid competing controller, fan or power-management services.

Do not guess fan curves or raise TDP limits. Establish idle/load temperatures, behaviour and power consumption first. Claims of better performance require repeatable baseline comparisons.

## Power, sleep and hibernation

Current Omarchy documentation describes independent AC/battery power preferences. Start with balanced or power-saving settings and measure usability.

Prioritise reliable lid close/resume, Wi-Fi recovery, low idle draw and overnight sleep drain. Hibernation is a separate test: current documentation describes a swap allocation approximately equal to RAM and a Limine dependency. Include that space in the budget.

Do not assume a successful suspend toggle proves that the device reaches an efficient sleep state.

## Maintainable profile structure

Build a small versioned FR3K GPD profile with:

- Shared non-secret FR3K preferences.
- GPD-specific display/input/power overrides.
- Optional development, Android and hardware groups.
- Installed-version manifest and compatibility notes.
- Idempotent application steps and rollback instructions.
- Explicit separation of public defaults and private device identity/credentials.

Use the stable update channel initially. Use Omarchy's supported updater, which coordinates package changes, migrations and snapshots; a plain package upgrade is not equivalent.

System snapshots restore the root filesystem, not the home directory or user configuration. Maintain separate backups of projects and dotfiles. Test recovery rather than assuming snapshots cover everything. A distribution reinstall may reset user configuration defaults.

## Acceptance matrix

All rows are PENDING until supported by actual device evidence.

| Area | Required validation |
|---|---|
| Triple boot | Windows, Fedora and Omarchy each boot successfully |
| EFI recovery | Independent firmware entries and rescue path verified |
| Display | Correct orientation and readable scaling |
| Touch | Accurate interaction across the entire panel |
| Controller | Buttons/sticks and mode switching work consistently |
| Audio | Speakers, headphones and microphone tested |
| Network | Wi-Fi/Bluetooth work and recover after sleep |
| Suspend | Repeated lid-close/resume cycles without hangs |
| Battery | Measured idle use and overnight sleep drain |
| Docking | External display and USB reconnect correctly |
| Thermals | Sustained workload behaviour measured without unsafe tuning |
| Development | Representative repository workflow succeeds |
| Hardware tools | Relevant serial/USB devices accessible with scoped permissions |
| Remote work | Jobs remain identifiable and results verifiable after disconnect |
| Updates | Supported update succeeds and recovery remains available |
| Backups | Configuration and personal-data restoration tested |

Record versions, test method, duration, results and failures. A successful boot is not full hardware acceptance; a running job is not success.

## Read-only Fedora inventory

Run on the GPD while booted into Fedora. These commands inspect state and do not resize or format storage. Some utilities may be absent; report that rather than substituting destructive commands.

```bash
cat /etc/os-release
cat /sys/class/dmi/id/product_name
cat /sys/class/dmi/id/product_version
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS
df -hT
sudo parted -l
sudo efibootmgr -v
mokutil --sb-state
```

Review output before sharing publicly; host details, labels and mount paths may be private. Keep raw device evidence in a private location and publish only sanitised findings.

## Next implementation gates

1. Receive and inspect the real disk/hardware inventory.
2. Confirm recovery material and usable free space.
3. Produce a partition-specific installation plan.
4. Validate installer version and applicable instructions.
5. Perform the physical install with the reviewed target layout.
6. Test triple boot and baseline hardware.
7. Apply customisations incrementally and record results.
8. Test update and recovery paths.

No partition-specific write commands are approved or supplied by this research document.

## Sources

Sources consulted during the conversation; these are live documentation pages, not immutable source snapshots.

1. [Omarchy website and advertised release](https://omarchy.org/)
2. [Getting started](https://omarchy.org/manual/getting-started/)
3. [Dual boot installation](https://omarchy.org/manual/dual-boot-install/)
4. [Dotfiles](https://omarchy.org/manual/dotfiles/)
5. [Monitor configuration](https://omarchy.org/manual/monitors/)
6. [Custom themes](https://omarchy.org/manual/making-your-own-theme/)
7. [Updates and channels](https://omarchy.org/manual/updates/)
8. [System snapshots](https://omarchy.org/manual/system-snapshots/)
9. [Security](https://omarchy.org/manual/security/)
10. [System sleep and power profiles](https://omarchy.org/manual/system-sleep/)
11. [Handheld Daemon upstream](https://github.com/hhd-dev/hhd)
12. [Hyprland configuration options](https://wiki.hypr.land/configuring/core/config-options/)
13. [Hyprland per-device configuration](https://wiki.hypr.land/configuring/core/devices/)
14. [Microsoft BitLocker overview](https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/)
15. [Framework Omarchy installation guidance](https://dozuki-prod-us-east-1-guide-pdfs.s3.amazonaws.com/pdf/framework/guide_568_en_1879.pdf)

## Publication boundary

This document preserves the substantive research and proposed setup while excluding private fleet addresses, credentials, raw device inventories and live infrastructure state. Research saved to GitHub is not installation, deployment or hardware verification.
