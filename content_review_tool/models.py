from pydantic import BaseModel, Field
from typing import List, Optional

class Suggestion(BaseModel):
    category: str = Field(description="The category of the suggestion (e.g., 'Tone', 'Compliance', 'Quality')")
    feedback: str = Field(description="Specific feedback on what is wrong or could be improved.")
    actionable_tip: str = Field(description="A clear instruction on how to fix the issue.")

class ReviewMetrics(BaseModel):
    tone_score: int = Field(description="0-100 score for how engaging and appropriate the tone is.")
    image_quality_score: int = Field(description="0-100 score for technical image quality (lighting, focus, composition).")
    caption_relevance_score: int = Field(description="0-100 score for how well the caption matches the image.")
    compliance_score: int = Field(description="0-100 score for adherence to ad guidelines (e.g., disclosure).")

class ReviewResult(BaseModel):
    metrics: ReviewMetrics
    suggestions: List[Suggestion]
    overall_score: int = Field(description="0-100 overall quality score.")
    summary: str = Field(description="A brief summary of the review.")
