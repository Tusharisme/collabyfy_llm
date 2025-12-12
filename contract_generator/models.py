from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class Party(BaseModel):
    name: str = Field(..., description="Legal name of the individual or company")
    email: str = Field(..., description="Contact email")
    address: Optional[str] = Field(None, description="Physical address")
    role: str = Field(..., description="'Influencer' or 'Brand'")

class Deliverable(BaseModel):
    description: str = Field(..., description="Description of the work product")
    platform: str = Field(..., description="e.g. Instagram, TikTok, YouTube")
    due_date: Optional[str] = Field(None, description="Due date string")
    format: Optional[str] = Field(None, description="e.g. Reel, Story, Post")

class PaymentTerms(BaseModel):
    total_amount: float = Field(..., description="Total contract value")
    currency: str = Field("USD", description="Currency code")
    schedule: str = Field(..., description="Natural language description of when payment happens (e.g. 50% upfront)")

class ContractRequest(BaseModel):
    brand: Party
    influencer: Party
    effective_date: str = Field(..., description="Date the contract becomes active")
    campaign_name: str
    deliverables: List[Deliverable]
    payment_terms: PaymentTerms
    exclusivity_clause: Optional[str] = Field(None, description="Custom exclusivity terms if needed")
    jurisdiction: str = Field("State of California", description="Governing law location")

class ContractContent(BaseModel):
    """The processed content ready for rendering"""
    title: str
    intro_text: str
    terms_text: List[str] # List of paragraphs or clauses
    schedule_a: str # The Deliverables section text
    schedule_b: str # The Payment section text
    signatures_section: str
