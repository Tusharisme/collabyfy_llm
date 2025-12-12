from llm_client import NegotiationLLM
from models import Message, ChatSession, NegotiationContext, LLMResponse
from strategies import NegotiationStrategy, CollaborativeStrategy

class NegotiationEngine:
    def __init__(self, strategy: NegotiationStrategy = None):
        self.llm = NegotiationLLM()
        self.strategy = strategy or CollaborativeStrategy()
        self.session: ChatSession = None

    def start_session(self, influencer_name: str, followers: str, engagement: str, budget: float) -> str:
        initial_offer = self.strategy.get_initial_offer(budget)
        target_price = self.strategy.get_target_price(budget)
        
        context = NegotiationContext(
            influencer_name=influencer_name,
            follower_count=followers,
            engagement_rate=engagement,
            max_budget=budget,
            initial_offer=initial_offer,
            target_price=target_price
        )
        
        self.session = ChatSession(
            history=[],
            metadata=context
        )
        # We don't necessarily send a message to LLM yet, just return status
        return f"Negotiation Strategy: {self.strategy.name}\nInitial Offer: ${initial_offer:.2f} (Budget: ${budget:.2f})"

    def process_message(self, user_text: str) -> LLMResponse:
        if not self.session:
            raise ValueError("Session not started.")
            
        print(f"DEBUG: Processing message: {user_text}")

        # Add user message to history
        self.session.history.append(Message(role="user", content=user_text))

        # Generate response
        response = self.llm.generate_response(self.session.history, self.session.metadata)
        
        print(f"DEBUG: Raw LLM Response: {response}")

        # GUARDRAILS
        if response.suggested_offer:
            if response.suggested_offer > self.session.metadata.max_budget:
                # Override!
                response.internal_thought += " [GUARDRAIL WARNING: AI tried to offer more than budget. Capped.]"
                response.suggested_offer = self.session.metadata.max_budget
                response.message_to_influencer = (
                     f"(Correction: I really cannot go above ${self.session.metadata.max_budget}.) " + 
                     response.message_to_influencer
                )
        
        # Add model response to history
        self.session.history.append(Message(role="model", content=response.message_to_influencer))
        
        return response
