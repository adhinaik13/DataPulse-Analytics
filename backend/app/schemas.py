from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EventIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_name: str = Field(min_length=1, max_length=80, strip_whitespace=True)
    user_id: str = Field(min_length=1, max_length=120, strip_whitespace=True)
    session_id: str = Field(min_length=1, max_length=120, strip_whitespace=True)
    country: str = Field(default="Unknown", min_length=1, max_length=80, strip_whitespace=True)
    device: str = Field(default="desktop", min_length=1, max_length=40, strip_whitespace=True)
    value: float = Field(default=0, ge=0, allow_inf_nan=False)
    occurred_at: datetime | None = None


class Metrics(BaseModel):
    events: int
    users: int
    sessions: int
    revenue: float
