from abc import ABC, abstractmethod

class NegotiationStrategy(ABC):
    """Abstract base class for negotiation strategies."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @abstractmethod
    def get_initial_offer(self, budget: float) -> float:
        """Calculate the starting offer based on the budget."""
        pass

    @abstractmethod
    def get_target_price(self, budget: float) -> float:
        """Calculate the ideal target price."""
        pass

class AggressiveStrategy(NegotiationStrategy):
    """Starts very low, aims to save maximum budget."""
    name = "Aggressive"
    
    def get_initial_offer(self, budget: float) -> float:
        return budget * 0.30  # Start at 30% of max
        
    def get_target_price(self, budget: float) -> float:
        return budget * 0.60  # Target 60% of max

class CollaborativeStrategy(NegotiationStrategy):
    """Fairer start to build relationship."""
    name = "Collaborative"
    
    def get_initial_offer(self, budget: float) -> float:
        return budget * 0.50  # Start at 50%
        
    def get_target_price(self, budget: float) -> float:
        return budget * 0.80  # Target 80%

class GenerousStrategy(NegotiationStrategy):
    """For high-value VIP influencers."""
    name = "Generous"
    
    def get_initial_offer(self, budget: float) -> float:
        return budget * 0.70  # Start high
        
    def get_target_price(self, budget: float) -> float:
        return budget * 0.95  # Willing to spend almost all
