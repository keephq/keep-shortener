from pydantic import BaseModel


class Url(BaseModel):
    is_active: bool
    target_url: str
    clicks: int = 0
