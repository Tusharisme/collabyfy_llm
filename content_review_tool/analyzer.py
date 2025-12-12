import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

from PIL import Image

# For relative imports when running as a module, or simple imports when running locally
try:
    from models import ReviewResult
except ImportError:
    from .models import ReviewResult

load_dotenv()

class ContentAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("API_KEY not found in environment variables.")
        genai.configure(api_key=self.api_key)
        
        # Configure model
        self.model = genai.GenerativeModel(
            "gemini-2.5-flash",
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=ReviewResult
            )
        )

    def analyze(self, image_path: str, caption: str) -> ReviewResult:
        """
        Analyzes an image and caption using Gemini 2.5 Flash.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")

        # Load image
        img = Image.open(image_path)
        
        prompt = f"""
        You are an expert Social Media Content Editor. Analyze this post (Image + Caption) and provide a structured review.
        
        Caption: "{caption}"
        
        Evaluate based on:
        1. Tone: Is it engaging?
        2. Image Quality: Lighting, composition, focus.
        3. Relevance: Does the caption match the image?
        4. Compliance: If it looks like an ad/promo, are disclosures present?
        
        Provide specific, actionable suggestions for improvement.
        """
        
        try:
            response = self.model.generate_content([prompt, img])
            return ReviewResult.model_validate_json(response.text)
        except Exception as e:
            # Handle potential schema/validation errors gracefully
            print(f"Error during analysis: {e}")
            raise e

if __name__ == "__main__":
    # Simple test
    pass
