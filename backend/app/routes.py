from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from .models import HealthStatus
from .db import get_conn
from .config import settings
from .services.voice_verifier import verifier
import sqlite3
import logging
import xml.etree.ElementTree as ET

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health", response_model=HealthStatus)
async def health():
    last_error = None
    db_ok = False
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        db_ok = True
        conn.close()
    except Exception as e:
        last_error = str(e)
    return HealthStatus(ready=True, db=db_ok, mock_mode=settings.MOCK_MODE, last_error=last_error)


@router.get("/metrics")
async def metrics():
    # Simple placeholder for Prometheus scraping
    return PlainTextResponse("# HELP vp_dummy A dummy metric\nvp_dummy 1\n")


@router.post("/calls/inbound")
async def inbound_call(request: Request):
    """
    Simulate a Twilio webhook receiving an inbound call. If semaphore is full,
    return TwiML busy response.
    Expected form fields: From, To
    For demo, we accept body or query args for transcript and speaker_score.
    """
    form = await request.form()
    transcript = form.get("transcript") or "hello world"
    speaker_score = float(form.get("speaker_score") or 0.5)

    # Try to acquire immediately
    sem = verifier._semaphore
    if sem.locked() and sem._value == 0:
        # Busy - return TwiML busy response
        twiml = ET.Element("Response")
        ET.SubElement(twiml, "Say").text = "All agents are currently busy. Please try again later."
        xml_str = ET.tostring(twiml, encoding="utf-8")
        return Response(content=xml_str, media_type="application/xml")

    result = await verifier.verify_call(transcript, speaker_score)
    return JSONResponse(result)
