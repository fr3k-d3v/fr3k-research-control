"""Opt-in llama.cpp tokenizer adapter for FR3K context planning.

The caller supplies the trusted endpoint and secret from its existing
credential store. Never write tokens, prompts or credentials to logs.
"""
import json
from urllib.request import Request, urlopen
from urllib.parse import urlsplit

class TokenizerError(RuntimeError):
    pass

def tokenize(content: str, *, base_url: str, api_key: str,
             timeout: float = 15.0) -> tuple[int, ...]:
    if not isinstance(content, str) or not api_key:
        raise ValueError("content and api_key required")
    parsed = urlsplit(base_url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc or parsed.username:
        raise ValueError("invalid tokenizer endpoint")
    url = base_url.rstrip("/") + "/tokenize"
    req = Request(url, data=json.dumps({"content": content}).encode(),
                  headers={"Content-Type": "application/json",
                           "Authorization": "Bearer " + api_key})
    try:
        with urlopen(req, timeout=timeout) as response:
            result = json.load(response)
        tokens = result.get("tokens")
        if not isinstance(tokens, list) or not all(type(x) is int for x in tokens):
            raise TokenizerError("unexpected tokenizer response")
        return tuple(tokens)
    except (OSError, ValueError, KeyError) as exc:
        raise TokenizerError("tokenization unavailable") from exc

def count(content: str, **kwargs) -> int:
    return len(tokenize(content, **kwargs))
