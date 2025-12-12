import google.generativeai as genai
import os
import typing
from models import LLMResponse, Message, NegotiationContext
from prompts import SYSTEM_PROMPT_TEMPLATE

class NegotiationLLM:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            # Fallback for when running in an env where load_dotenv wasn't called globally yet
            from dotenv import load_dotenv
            load_dotenv()
            self.api_key = os.getenv("API_KEY")
            
        if not self.api_key:
             raise ValueError("API_KEY not found. Please set it in the .env file.")
             
        genai.configure(api_key=self.api_key)

    def generate_response(self, history: list[Message], context: NegotiationContext) -> LLMResponse:
        """
        Generates a structured negotiation response from Gemini.
        """
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            influencer_name=context.influencer_name,
            follower_count=context.follower_count,
            engagement_rate=context.engagement_rate,
            max_budget=context.max_budget,
            target_price=context.target_price,
            initial_offer=context.initial_offer
        )

        # Convert Pydantic messages to Gemini format
        chat_history = []
        for msg in history:
            if msg.role == "user":
                chat_history.append({"role": "user", "parts": [msg.content]})
            elif msg.role == "model":
                chat_history.append({"role": "model", "parts": [msg.content]})
            # System role is handled via system_instruction
        
        # Configure model with structured output enforcement
        model = genai.GenerativeModel(
            "gemini-2.5-flash",
            system_instruction=system_prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=LLMResponse
            )
        )

        try:
            # If history is empty, start chat. If not, continue.
            # But generate_content is stateless unless using chat. 
            # We want to pass the whole history each time for stateless simplicity or use start_chat.
            # Using generate_content directly with a list of contents acts as a chat history if formatted right?
            # Actually, `generate_content` takes `contents`. If `contents` is a list, it treats it as multi-turn?
            # Yes, if valid roles are used.
            
            response = model.generate_content(chat_history)
            
            # Parse the JSON response into our Pydantic model
            return LLMResponse.model_validate_json(response.text)
            
        except Exception as e:
            # Fallback or error handling
            print(f"LLM Generation Error: {e}")
            # Return a safe fallback to prevent crash
            return LLMResponse(
                message_to_influencer="I'm sorry, I'm having trouble processing that right now. Could we pause for a moment?",
                internal_thought=f"Error occurred: {str(e)}",
                is_deal_reached=False,
                is_deal_lost=False,
                confidence_score=0.0
            )
