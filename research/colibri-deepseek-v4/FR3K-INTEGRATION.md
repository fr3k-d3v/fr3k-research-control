# FR3K integration architecture

## Boundary

Colibrì is a model runtime and local inference provider. It is not FR3K's orchestrator, durable job system, policy engine, memory authority or device-control plane.

FR3K remains responsible for:

- Job IDs, dependencies, idempotency, leases, fencing and immutable terminal states.
- OBSERVE / AUTO / APPROVAL / PHYSICAL authority boundaries.
- Tool registry, allowlists, schema validation, approvals and execution.
- Evidence capture, provenance, audit records and reconciliation.
- User/device identity, access control, secrets and data retention.
- Retry budgets, deadlines, cancellation and recovery.
- Provider routing and fallback.

Colibrì receives bounded inference requests and returns model output. Model output is untrusted data until FR3K validates it.

## Proposed provider topology

~~~text
FR3K orchestrator
  ├── policy / authority / job state
  ├── evidence store and verification
  ├── tool registry + execution sandbox
  └── inference provider interface
        ├── Colibrì / DeepSeek V4 Flash (local candidate)
        ├── llama.cpp / current Qwen baseline
        └── hosted providers (existing configuration)
~~~

The initial integration should be a provider adapter, not a fork of Colibrì and not a replacement for the FR3K job protocol.

## Colibrì interface

The upstream API guide documents:

- OpenAI-compatible POST /v1/chat/completions.
- Anthropic-compatible POST /v1/messages.
- GET /v1/models and model metadata.
- COLI_API_KEY bearer authentication.
- Local bind example 127.0.0.1:8000.
- OpenAI tools and Anthropic tool_use for DeepSeek V4.
- DeepSeek V4 native DSML tool-call parsing.

Use the served model ID from runtime status / GET /v1/models; do not hardcode a model ID before observing the actual configured server.

## Important runtime constraints

- The DeepSeek V4 engine guide documents greedy serving and one KV slot. Do not assume multiple simultaneous independent sessions. Serialize requests or isolate engines until concurrency behavior is measured.
- Grammar forcing is documented as unsupported for DeepSeek V4. JSON-mode and tool-call reliability must be tested; do not assume constrained decoding.
- tool_choice required is a prompt-level instruction, not a hard sampler constraint. Validate returned tool calls and arguments.
- MTP/speculative drafting exists but is off by default in the DeepSeek V4 engine guide. Treat it as a later isolated experiment.
- The documented Colibrì cluster worker path covers GLM and DeepSeek V4.1, not DeepSeek V4. Do not claim that Colibrì can shard this V4 model across the FR3K fleet.
- Colibrì's own MCP server is for managing its runtime; it does not replace FR3K MCP/Fleet authority.

## Request lifecycle

1. FR3K creates a stable job ID and validates the task's authority class.
2. FR3K selects the Colibrì provider only when the model capability profile and resource state permit it.
3. FR3K sends a bounded request with a timeout, output ceiling, request ID and only the context needed for the task.
4. Colibrì returns text and/or tool-call proposals.
5. FR3K validates response structure, tool name, argument schema, policy and approval requirements.
6. FR3K executes only allowlisted tools under the job's authority and lease.
7. FR3K stores raw tool results and evidence before deriving conclusions.
8. FR3K sends tool results back for continuation, bounded by a step and token budget.
9. FR3K verifies the resulting artifact or action independently and records the terminal state.

A model response cannot self-approve an action, extend its own authority, alter a lease, change job state or claim that a tool succeeded.

## Security requirements

- Bind to loopback by default and set COLI_API_KEY.
- Do not expose the endpoint to LAN, Tailscale or the public internet until an authenticated reverse-proxy and threat review exists.
- Keep API keys and provider secrets in the local secret store / environment, never in Git.
- Do not place private prompts, customer data, device identifiers or raw logs in this public research repository.
- Treat prompt injection, tool-call text, model-generated URLs and retrieved documents as untrusted.
- Apply strict request, response, concurrency, time and memory budgets.
- Provide a kill switch and a fallback route to the existing llama.cpp provider.
- Record model revision, quant, runtime commit and backend with every inference result.

## Capability profile to implement

~~~yaml
provider_id: colibri-deepseek-v4
status: experimental
model_family: deepseek-v4-flash
model_revision: ""
quantization: ""
runtime_commit: ""
backend: ""
context_limit_tested: null
concurrency_tested: null
tool_calls: supported-by-upstream-needs-local-validation
grammar_constrained_output: unsupported-by-upstream-docs
speculative_decoding: off-until-separately-tested
network_scope: loopback-only
fallback_provider: current-llama-cpp
authority: inference-only
~~~

## FR3K integration acceptance

- [ ] Adapter can health-check without confusing readiness with completed work.
- [ ] Requests have stable IDs, deadlines, cancellation and bounded retries.
- [ ] Provider failure falls back without duplicating tool execution.
- [ ] Tool calls are schema-validated and allowlisted.
- [ ] Approval-required actions remain blocked pending human approval.
- [ ] Tool results and evidence are retained independently of model summaries.
- [ ] Multi-turn tool loop passes a harmless end-to-end test.
- [ ] Model version, backend, quant and usage are recorded.
- [ ] Current llama.cpp route remains available and recoverable.
