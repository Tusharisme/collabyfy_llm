from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class LLMResponse(BaseModel):
    message_to_influencer: str = Field(..., description="The persuasive message to send to the influencer.")
    internal_thought: str = Field(..., description="Reasoning behind the message and offer strategy.")
    is_deal_reached: bool = Field(..., description="True if the influencer has explicitly accepted the offer.")
    is_deal_lost: bool = Field(..., description="True if the negotiation has explicitly failed or influencer rejected final offer.")
    suggested_offer: Optional[float] = Field(description="The specific monetary offer made in this message, if any. Null if no specific number mentioned.")
    confidence_score: float = Field(..., description="0.0 to 1.0 score of how likely the deal is to close successfully.")

class NegotiationContext(BaseModel):
    influencer_name: str
    follower_count: str
    engagement_rate: str
    max_budget: float
    initial_offer: float
    target_price: float 

class Message(BaseModel):
    role: Literal["user", "model", "system"] # Gemini uses 'user' and 'model'
    content: str

class ChatSession(BaseModel):
    history: List[Message] = []
    metadata: NegotiationContext
