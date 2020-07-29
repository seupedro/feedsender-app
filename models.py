from typing import Optional
from pydantic import BaseModel


class Message(BaseModel):
    chat_id: int
    text: str
    parse_mode: Optional[str]
    disable_web_page_preview: bool = False
    disable_notification: bool = False
    reply_to_message_id: Optional[int]
    reply_markup: Optional[str]
    timeout: Optional[float]
