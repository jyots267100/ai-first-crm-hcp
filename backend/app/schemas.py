from typing import Optional, List, Any, Dict
from pydantic import BaseModel


class InteractionData(BaseModel):
    id: Optional[int] = None
    hcp_name: Optional[str] = None
    interaction_type: Optional[str] = "Meeting"
    interaction_date: Optional[str] = None
    interaction_time: Optional[str] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[List[str]] = []
    samples_distributed: Optional[List[Dict[str, Any]]] = []
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    follow_up_actions: Optional[str] = None


class ChatRequest(BaseModel):
    message: str
    interaction_id: Optional[int] = None


class ChatResponse(BaseModel):
    message: str
    tool_used: Optional[str] = None
    interaction: Optional[InteractionData] = None