"""
Lightweight Gemini client wrapper with token-limited prompt handling.
This is a mock-capable implementation. It estimates tokens and truncates the prompt
if necessary. In MOCK_MODE it returns deterministic responses.
"""
from typing import Dict
from ..config import settings
import hashlib
import time
import logging

logger = logging.getLogger(__name__)


def estimate_tokens(text: str) -> int:
    # Very rough estimator: 4 chars ~ 1 token
    return max(1, len(text) // 4)


GEMINI_PROMPT_TEMPLATE = """
You are a corporate voice verification assistant.
Instructions: Verify speaker identity from audio transcript and speaker score.
Limit the response tokens to {max_resp} tokens.
Context:
{context}
"""


def build_prompt(context: str, max_resp: int = None) -> str:
    if max_resp is None:
        max_resp = settings.MAX_GEMINI_RESPONSE_TOKENS
    prompt = GEMINI_PROMPT_TEMPLATE.format(max_resp=max_resp, context=context)
    # Enforce AI_TOKEN_LIMIT by truncation if needed
    token_count = estimate_tokens(prompt)
    if token_count > settings.AI_TOKEN_LIMIT:
        # Truncate context deterministically
        allowed = int(len(context) * (settings.AI_TOKEN_LIMIT / token_count)) - 100
        context_trunc = context[:max(0, allowed)]
        prompt = GEMINI_PROMPT_TEMPLATE.format(max_resp=max_resp, context=context_trunc)
        logger.info("Prompt truncated to respect AI_TOKEN_LIMIT")
    return prompt


def call_gemini(prompt: str, mock_seed: str = "seed") -> Dict:
    """
    Mock behavior: deterministic hash of prompt + seed returns consistent reply.
    Real integration would call the provider API and respect token limits.
    """
    if settings.MOCK_MODE or not settings.AI_PROVIDER_API_KEY:
        key = (prompt + mock_seed).encode("utf-8")
        digest = hashlib.sha256(key).hexdigest()
        # deterministic pseudo-response
        resp = {
            "decision": "accept" if int(digest[:8], 16) % 2 == 0 else "reject",
            "confidence": (int(digest[8:16], 16) % 100) / 100.0,
            "explain": "Mocked deterministic response",
            "tokens_used": estimate_tokens(prompt) + 10,
        }
        time.sleep(settings.RESPONSE_DELAY_MS / 1000.0)
        return resp

    # TODO: Implement real provider call using settings.AI_PROVIDER_API_KEY
    logger.warning("Real Gemini integration not implemented; falling back to mock.")
    return call_gemini(prompt, mock_seed)
