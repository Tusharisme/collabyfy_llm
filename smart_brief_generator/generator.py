import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Robust import handling
try:
    from models import BriefData, BriefRequest
except ImportError:
    from .models import BriefData, BriefRequest

load_dotenv()

class BriefContentGenerator:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("API_KEY not found. Please check .env file.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            "gemini-2.5-flash",
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=BriefData
            )
        )

    def generate(self, request: BriefRequest) -> BriefData:
        prompt = f"""
        You are a Campaign Manager. Create a detailed Influencer Campaign Brief based on the following:
        
        Brand: {request.brand_name}
        Topic: {request.campaign_topic}
        Audience: {request.target_audience or "General"}
        Focus: {request.key_message_focus or "Brand Awareness"}
        
        Output a valid JSON object matching the schema.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return BriefData.model_validate_json(response.text)
        except Exception as e:
            print(f"Error generating brief content: {e}")
            raise e
