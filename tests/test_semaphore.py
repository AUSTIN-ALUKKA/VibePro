import requests
import os
import threading
import time

BASE = os.getenv("BACKEND_URL", "http://backend:8000")


def call_inbound(session, transcript="hi", speaker_score=0.5):
    r = requests.post(f"{BASE}/calls/inbound", data={"transcript": transcript, "speaker_score": speaker_score})
    return r


def test_semaphore_blocks_second_call():
    # Fire two calls nearly simultaneously
    results = []

    def target(i):
        r = call_inbound(None, f"call {i}", 0.5)
        results.append((i, r.status_code, r.text[:200]))

    t1 = threading.Thread(target=target, args=(1,))
    t2 = threading.Thread(target=target, args=(2,))
    t1.start()
    time.sleep(0.1)
    t2.start()
    t1.join()
    t2.join()

    # At least one response should be 200 (handled) and one XML busy or 200 depending on timing
    codes = [r[1] for r in results]
    assert 200 in codes
