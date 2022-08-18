from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    uniq_id: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
