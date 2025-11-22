import asyncio
import logging
from typing import Optional
from ..config import settings
from ..services.gemini_client import build_prompt, call_gemini

logger = logging.getLogger(__name__)


class Verifier:
    def __init__(self):
        self._max_concurrent = max(1, settings.MAX_CONCURRENT_CALLS)
        self._semaphore = asyncio.Semaphore(self._max_concurrent)

    async def verify_call(self, transcript: str, speaker_score: float) -> dict:
        """Main verification flow. Uses Gemini mock or real API via gemini_client."""
        # Simple guard: ensure semaphore enforces single-call concurrency
        async with self._semaphore:
            try:
                prompt = build_prompt(f"Transcript:\n{transcript}\nSpeaker score: {speaker_score}")
                resp = call_gemini(prompt)
                result = {
                    "decision": resp.get("decision", "reject"),
                    "confidence": resp.get("confidence", 0.0),
                    "explain": resp.get("explain", ""),
                }
                logger.info("Verification result", extra={"result": result})
                return result
            except Exception as e:
                logger.exception("Verification failed")
                # Circuit-breaker-like: fallback deterministic rule
                return {
                    "decision": "reject",
                    "confidence": 0.0,
                    "explain": f"Fallback due to error: {e}",
                }


verifier = Verifier()
