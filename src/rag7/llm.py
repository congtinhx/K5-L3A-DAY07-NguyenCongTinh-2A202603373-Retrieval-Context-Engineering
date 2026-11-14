"""Minimal OpenAI-compatible chat-completions client with tool calling (stdlib only).

Works with OpenAI (default) or any compatible endpoint via OPENAI_BASE_URL
(e.g. OpenRouter). Retries 429/5xx; other errors propagate so they are logged
as provider errors, never replaced by fake output.
"""
import json
import os
import time
import urllib.error
import urllib.request

# USD per 1M tokens (input, output). Check the provider price page; unknown models -> cost None.
PRICES = {
    'gpt-4o-mini': (0.15, 0.60),
    'gpt-4.1-mini': (0.40, 1.60),
    'gpt-4.1-nano': (0.10, 0.40),
    'gpt-4o': (2.50, 10.00),
}


class ProviderError(RuntimeError):
    pass


def cost_usd(model: str, prompt_tokens: int, completion_tokens: int) -> float | None:
    price = PRICES.get(model)
    if not price:
        return None
    return (prompt_tokens * price[0] + completion_tokens * price[1]) / 1_000_000


class OpenAIChat:
    def __init__(self, model: str, *, temperature: float = 0.0, timeout: int = 60, retries: int = 3):
        self.api_key = os.getenv('OPENAI_API_KEY', '').strip()
        if not self.api_key:
            raise ProviderError('Thiếu OPENAI_API_KEY trong .env')
        self.base_url = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1').rstrip('/')
        self.model, self.temperature, self.timeout, self.retries = model, temperature, timeout, retries

    def chat(self, messages: list[dict], tools: list[dict], tool_choice='required') -> dict:
        body = {'model': self.model, 'messages': messages, 'tools': tools, 'tool_choice': tool_choice,
                'temperature': self.temperature, 'parallel_tool_calls': False}
        data = json.dumps(body).encode('utf-8')
        last = None
        for attempt in range(self.retries + 1):
            req = urllib.request.Request(f'{self.base_url}/chat/completions', data=data, method='POST',
                                         headers={'Authorization': f'Bearer {self.api_key}',
                                                  'Content-Type': 'application/json'})
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    return json.loads(resp.read().decode('utf-8'))
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode('utf-8', 'replace')[:500]
                last = ProviderError(f'HTTP {exc.code}: {detail}')
                if exc.code not in (429, 500, 502, 503, 504):
                    raise last from exc
            except (urllib.error.URLError, TimeoutError) as exc:
                last = ProviderError(f'Network: {exc}')
            time.sleep(2 ** attempt)
        raise last
