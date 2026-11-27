---
description: Reconcile Fleet job status and output without dispatching or promoting a release.
---

Use the supplied exact Fleet job ID. If absent, report BLOCKED rather than guessing. Query authenticated Fleet jobs_status and command_status tools for the same ID. If either tool is unavailable, report UNKNOWN. Do not run shell commands, create jobs, grant approvals, cancel work or change any device. Compare identity, terminal flag, status, exit code, approval state and truncation; if records disagree, re-observe once, then report UNKNOWN. A succeeded execution is not requirement verification. Check the requested acceptance criteria against actual complete output and evidence kind. Do not expose raw private logs or identifiers in public artifacts. Never mark simulated, absent or unauthenticated physical evidence as verified. Return a sanitized result with state, evidence limitations and next required gate. The existing Fleet server alone controls authority and scheduling.
