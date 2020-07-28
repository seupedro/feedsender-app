from typing import Optional
from pydantic import BaseModel


class Message(BaseModel):
    chat_id: int
    text: Optional[str]
