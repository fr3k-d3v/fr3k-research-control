"""FR3K conservative Hermes context engine.

Extends Hermes' native compressor. Request-only pruning is intentionally
limited to simple text conversations without tool calls; tool-containing
sessions delegate to Hermes' existing compression implementation.
"""
from agent.context_compressor import ContextCompressor

class FR3KContextEngine(ContextCompressor):
    def __init__(self):
        super().__init__(model="fr3kc0d3r", threshold_percent=0.5,
                         protect_first_n=3, protect_last_n=20,
                         summary_target_ratio=0.2)

    @property
    def name(self):
        return "fr3k64k"

    def select_context(self, request_messages, *, conversation_messages=None,
                       incoming_message=None, budget_tokens=None, **kwargs):
        # Never change structured/tool messages, images or non-chat content.
        if not isinstance(request_messages, list):
            return request_messages
        if any(not isinstance(m, dict) or m.get("role") not in
               {"system", "developer", "user", "assistant"} or
               not isinstance(m.get("content"), str) for m in request_messages):
            return request_messages
        if len(request_messages) <= 24:
            return request_messages
        # Conservative character-based trigger; not a substitute for exact
        # tokenizer accounting. Native compressor remains the primary gate.
        limit = min(int(budget_tokens or 65536), 65536)
        if sum(len(m["content"]) for m in request_messages) < limit * 2:
            return request_messages
        # Preserve all privileged instructions, the most recent 20 messages,
        # and the newest user message. Drop only complete old user/assistant
        # pairs. Avoid pruning if the prefix is not pair-aligned.
        cutoff = max(0, len(request_messages) - 20)
        start = 0
        while start < cutoff and request_messages[start]["role"] in ("system", "developer"):
            start += 1
        middle = request_messages[start:cutoff]
        if len(middle) % 2 or any(middle[i]["role"] != "user" or
                                  middle[i+1]["role"] != "assistant"
                                  for i in range(0, len(middle), 2)):
            return request_messages
        return request_messages[:start] + request_messages[cutoff:]

def register(ctx):
    ctx.register_context_engine(FR3KContextEngine())
