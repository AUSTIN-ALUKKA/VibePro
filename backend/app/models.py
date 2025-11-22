from pydantic import BaseModel
from typing import Optional


class HealthStatus(BaseModel):
    ready: bool
    db: bool
    mock_mode: bool
    last_error: Optional[str] = None


class Enrollment(BaseModel):
    id: str
    name: str
    voiceprint: Optional[bytes] = None
