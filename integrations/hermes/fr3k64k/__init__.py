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

    def update_model(self, *args, **kwargs):
        # Never advertise more context than the local 65,536-token backend.
        supplied = kwargs.get("context_length")
        if supplied is None or supplied > 65536:
            kwargs["context_length"] = 65536
        result = super().update_model(*args, **kwargs)
        self.threshold_percent = 0.5
        return result

    @property
    def name(self):
        return "fr3k64k"

    def select_context(self, request_messages, *, conversation_messages=None,
                       incoming_message=None, budget_tokens=None, **kwargs):
        # Never discard conversation turns, tool pairs, instructions, or
        # evidence unless the caller explicitly marks it disposable.
        # Native Hermes compression handles long conversation histories.
        if not isinstance(request_messages, list):
            return request_messages
        if not all(isinstance(m, dict) for m in request_messages):
            return request_messages
        # A future retrieval layer may attach ephemeral optional passages.
        # Remove only those at pressure, never ordinary dialogue.
        limit = min(int(budget_tokens or 65536), 65536)
        if sum(len(str(m.get("content", ""))) for m in request_messages) < limit * 2:
            return request_messages
        return [{k: v for k, v in m.items() if k != "_fr3k_optional"}
                for m in request_messages if not m.get("_fr3k_optional", False)]

def register(ctx):
    ctx.register_context_engine(FR3KContextEngine())
