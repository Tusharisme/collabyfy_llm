import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import List
from models import ContractRequest, ContractContent

load_dotenv()

class ContractGenerator:
    def __init__(self):
        api_key = os.getenv("API_KEY")
        if not api_key:
            raise ValueError("API_KEY not found in .env")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def _generate_schedule_a(self, deliverables: list) -> str:
        """Uses AI to turn list of deliverables into a legal 'Services' description"""
        prompt = f"""
        You are a legal assistant drafting 'Schedule A: Services' for an influencer marketing agreement.
        Convert the following list of deliverables into a professional, clear, and legally binding list of services.
        Do not add introductory text. Just provide the clause text. Use bullet points or numbered lists where appropriate.
        
        Deliverables:
        {deliverables}
        """
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def _generate_schedule_b(self, payment_terms) -> str:
        """Uses AI to formulate the Payment Terms section"""
        prompt = f"""
        You are a legal assistant drafting 'Schedule B: Compensation' for an influencer marketing agreement.
        Draft the compensation clause based on these terms:
        Total: {payment_terms.total_amount} {payment_terms.currency}
        Schedule: {payment_terms.schedule}
        
        Ensure it clearly states when payment is due and any requirements for invoicing.
        Do not add introductory text. Just provide the clause text.
        """
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def generate(self, request: ContractRequest) -> ContractContent:
        # 1. Hybrid: Generate the variable parts with AI
        schedule_a_text = self._generate_schedule_a(request.deliverables)
        schedule_b_text = self._generate_schedule_b(request.payment_terms)

        # 2. Fixed: Standard Legal Boilerplate
        intro = (
            f"This INFLUENCER MARKETING AGREEMENT (the 'Agreement') is made effective as of {request.effective_date} "
            f"by and between {request.brand.name} ('Brand') and {request.influencer.name} ('Influencer').\n\n"
            "WHEREAS, Brand wishes to engage Influencer to provide certain content and social media services, and "
            "Influencer agrees to provide such services under the terms set forth herein."
        )

        terms = [
            "1. SERVICES. Influencer shall provide the services and deliverables described in Schedule A (the 'Services'). Influencer shall perform the Services in a professional manner.",
            
            "2. COMPENSATION. In full consideration for the Services, Brand shall pay Influencer the amount(s) set forth in Schedule B.",
            
            "3. INTELLECTUAL PROPERTY. Unless otherwise agreed in writing, Influencer grants Brand a non-exclusive, worldwide, royalty-free license to use the Deliverables for the period and purposes specified in this Agreement. Influencer represents they own all rights to the Content.",
            
            f"4. EXCLUSIVITY. {request.exclusivity_clause if request.exclusivity_clause else 'This Agreement does not create an exclusive relationship between the parties.'}",
            
            "5. INDEPENDENT CONTRACTOR. Influencer is an independent contractor and not an employee of Brand.",
            
            f"6. GOVERNING LAW. This Agreement shall be governed by the laws of {request.jurisdiction}.",
            
            "7. ENTIRE AGREEMENT. This Agreement constitutes the entire understanding between the parties."
        ]
        
        signatures = "IN WITNESS WHEREOF, the parties have executed this Agreement."

        return ContractContent(
            title=f"INFLUENCER AGREEMENT: {request.campaign_name.upper()}",
            intro_text=intro,
            terms_text=terms,
            schedule_a=schedule_a_text,
            schedule_b=schedule_b_text,
            signatures_section=signatures
        )
