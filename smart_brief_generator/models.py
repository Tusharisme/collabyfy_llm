from pydantic import BaseModel, Field
from typing import List, Optional

class BriefRequest(BaseModel):
    brand_name: str = Field(description="Name of the brand.")
    campaign_topic: str = Field(description="Short description or topic of the campaign (e.g. 'Summer Cold Brew Launch').")
    target_audience: Optional[str] = Field(None, description="Target demographic.")
    key_message_focus: Optional[str] = Field(None, description="Main vibe or message to convey.")

class BriefData(BaseModel):
    campaign_title: str = Field(description="A catchy title for the campaign.")
    overview: str = Field(description="2-3 paragraphs describing the campaign context and goals.")
    target_audience_description: str = Field(description="Detailed description of who we are talking to.")
    key_messages: List[str] = Field(description="List of 3-5 key selling points or messages.")
    deliverables: List[str] = Field(description="List of expected content pieces (e.g. '1 Reel', '3 Stories').")
    dos_and_donts: List[str] = Field(description="List of guidelines (e.g. 'Do use natural light', 'Don't mention competitors').")
    hashtags: List[str] = Field(description="List of required hashtags.")
