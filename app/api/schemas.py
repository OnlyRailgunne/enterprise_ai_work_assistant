from uuid import UUID

from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: UUID
    message: str


class ApprovalRequest(BaseModel):
    session_id: UUID
    approved: bool