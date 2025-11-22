from fastapi import FastAPI
from .routes import router
from .logging_config import configure_logging
from .db import ensure_db
from .config import settings

configure_logging()
ensure_db()

app = FastAPI(title="Voice Verification Interceptor")
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    # placeholder for startup tasks
    pass
