# FR3K Fabric — reuse-first GitHub landscape

**Checked:** 2026-11-09 ~18:06 AEST. **Evidence:** GitHub REST repository metadata retrieved using authenticated `gh api`; descriptions, licenses and last-push times reflect upstream metadata, **not** FR3K compatibility tests. No dependencies installed or deployed. Public document: do not add private fleet details.

## Decision: do not rebuild commodity infrastructure
Build only FR3K-specific capability and authority adapters. Keep **existing Fleet MCP** as interface; **one durable job orchestrator** behind it. Avoid running Windmill, Temporal, Prefect and AWX as competing authorities. Choose a single durable state engine after a minimal failure-test spike. Reuse ADB/Appium, Tailscale, OpenTelemetry, NATS and firmware tooling as subordinate components.

## Evaluated repositories and adoption recommendations
| Repository | GitHub status checked | Reuse for FR3K | Decision / risk |
|---|---|---|---|
| [temporalio/temporal](https://github.com/temporalio/temporal) | active; MIT; 2026-11-09 | durable workflow history, retries, timers, crash recovery | **SPIKE** vs existing Fleet MCP/Postgres; don't install in production before checking operational cost and authoritative job mapping |
| [windmill-labs/windmill](https://github.com/windmill-labs/windmill) | active; license metadata NOASSERTION; 2026-11-09 | scripts, scheduled research scans, internal dashboards, human approvals | **PILOT for non-authoritative research tasks only**; license/features must be audited; do not duplicate job state |
| [PrefectHQ/prefect](https://github.com/PrefectHQ/prefect) | active; Apache-2.0; 2026-11-09 | research ETL and retries | **ALTERNATIVE**, not concurrent scheduler |
| [dagster-io/dagster](https://github.com/dagster-io/dagster) | active; Apache-2.0; 2026-11-07 | asset provenance/data lineage | **DEFER**; evidence store can initially be simpler |
| [nats-io/nats-server](https://github.com/nats-io/nats-server) | active; Apache-2.0; 2026-11-06 | durable pub/sub between machines | **ADOPT WHEN NEEDED** as transport, not authority; at-least-once messages require idempotency/fencing |
| [tailscale/tailscale](https://github.com/tailscale/tailscale) | active; BSD-3-Clause; 2026-11-08 | secure device connectivity | **REUSE EXISTING** tailnet/grants, audit access; connection != approval |
| [open-telemetry/opentelemetry-collector](https://github.com/open-telemetry/opentelemetry-collector) | active; Apache-2.0; 2026-11-07 | unified telemetry/evidence correlation | **ADOPT** with secret-redaction and stable job IDs |
| [DeviceFarmer/stf](https://github.com/DeviceFarmer/stf) | active; license metadata NOASSERTION; 2026-11-09 | physical Android device farm, remote screen/ADB, reservation | **PILOT** with test phones; upstream warns of internal-process security assumptions, isolate from public internet |
| [appium/appium](https://github.com/appium/appium) | active; Apache-2.0; 2026-11-09 | Android UI automation, regression tests | **ADOPT** for overlay queue, rotation, Fold layout, crash/voice UI flows; real microphone remains hardware gate |
| [ansible/awx](https://github.com/ansible/awx) | active; license metadata NOASSERTION; 2026-11-09 | machine provisioning and repeatable configuration | **REUSE Ansible concepts**, AWX optional; not job orchestrator |
| [openremote/core](https://github.com/openremote/core) | active; license metadata NOASSERTION; 2026-11-09 | device registry, IoT protocols, dashboards | **REFERENCE/PILOT** for embedded assets; likely heavier than needed for initial fleet |
| [eclipse-kura/kura](https://github.com/eclipse-kura/kura) | active; EPL-2.0; 2026-11-08 | edge gateways, sensor/device management | **REFERENCE** for routers/gateways, not MCU firmware replacement |
| [eclipse-zenoh/zenoh](https://github.com/eclipse-zenoh/zenoh) | active; license metadata NOASSERTION; 2026-11-09 | distributed pub/sub/query for constrained links | **SPIKE** for intermittent edge/Reticulum-adjacent transport; do not assume native Reticulum compatibility |
| [eclipse-hono/hono](https://github.com/eclipse-hono/hono) | active; EPL-2.0; 2026-11-03 | IoT telemetry ingress | **DEFER** until many devices justify it |
| [actions/runner](https://github.com/actions/runner) | active; MIT; 2026-11-09 | CI builds and tests | **ADOPT CI where safe**; no direct privileged fleet authority from PR code |
| [go-task/task](https://github.com/go-task/task) | active; MIT; 2026-11-09 | repeatable developer task entrypoints | **ADOPT** if simpler than existing scripts |

`meshcentral/meshcentral` and `menderio/mender` lookups returned GitHub 404 for those exact paths; **UNKNOWN** canonical repository identity, not evidence projects don't exist. Search correct upstream before decisions.

## Existing FR3K work to preserve, not rewrite
- Existing Fleet MCP command, device registry and approval flow: inspect implementation and extend rather than fork a new dispatcher.
- Omarchy GPU exclusive lock and local-coder acceptance runner: reuse as GPU worker backend; preserve current validation and rollback.
- Contabo Gitea: reuse existing Git service; authenticated mirroring still BLOCKED/UNVERIFIED.
- Existing research ledger and private GPU source: GitHub system of record; never push secrets/raw private evidence to public repo.
- Android overlay media scripts and test devices: wrap in idempotent job adapters rather than recreate processing algorithms.

## Minimal integration blueprint
**Existing Fleet MCP** -> `FR3K job API` -> `single durable state store` -> `resource lease/fencing` -> typed `worker adapters` -> artifact digest and independent verifier. Tailscale protects transport; OpenTelemetry observes; NATS optional for event fan-out; Appium/DeviceFarmer run subordinate Android tests; Ansible handles configuration, not job decisions.

## Build-versus-reuse matrix
- **Reuse:** VPN, Android automation, workflow durability primitives, telemetry, CI, firmware flashing libraries, message transport, dashboards where compatible.
- **Build:** FR3K device capability schema; resource-aware GPU/phone/board placement; approval authority boundary; fencing and immutable outcomes; evidence semantics; hardware-specific regression packs; research-to-experiment ranking; Git provenance and release gates.
- **Do not build:** a new VPN, generic message broker, Android remote control UI, generic workflow language, generic tracing stack, or another LLM inference engine before reproducible comparison.

## Next validation work (do not claim completed)
1. Audit current Fleet MCP code for existing durable state, approvals, worker identities, retries, job IDs and lease enforcement. Compare with Temporal and Postgres-outbox prototypes on a non-production sandbox.
2. Test one crash/retry/duplicate dispatch scenario with **no GPU execution**; require stable job ID and monotonic fencing.
3. Pilot Appium with one emulator, then one Android phone, collecting reproducible overlay regressions.
4. Pilot telemetry using one trace across Contabo -> Omarchy -> artifact verification without logging secrets.
5. Check each dependency's actual license file, supported versions, maintenance/security advisories and resource costs before incorporation.
6. Produce a dependency lockfile, SBOM, pinned upstream SHAs and rollback plan for each adopted component.

## Reconciliation with connection-layer plan
This report narrows `FR3K-CONNECTION-LAYER-PLAN.md`: **Postgres outbox remains a low-risk initial candidate**, but Temporal should be benchmarked as an alternative *before* implementing a full home-grown durable workflow engine. Windmill/Prefect are research-workflow options, not additional job authorities. No adoption is verified until a bounded spike passes failure tests.
