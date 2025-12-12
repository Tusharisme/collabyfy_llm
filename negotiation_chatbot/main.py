import os
import sys
from dotenv import load_dotenv

# Ensure we can find the modules if running from here
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from engine import NegotiationEngine
except ImportError:
    # Fallback if running from outside without -m
    print("Error: Could not import engine. logic. Please run this script from inside the 'negotiation_chatbot' directory.")
    sys.exit(1)

def main():
    # Load env from this folder
    load_dotenv()
    
    print("=========================================")
    print("   Messaging & Negotiation Chatbot CLI   ")
    print("=========================================")
    print("Simulating integration with 'influencer_extractor'...")
    
    name = input("Influencer Name [Fashionista123]: ") or "Fashionista123"
    followers = input("Followers [150k]: ") or "150k"
    eng = input("Engagement [3.5%]: ") or "3.5%"
    budget_str = input("Max Budget ($) [1000]: ") or "1000"
    
    try:
        budget = float(budget_str)
    except ValueError:
        print("Invalid budget. Using 1000.")
        budget = 1000.0
    
    engine = NegotiationEngine()
    print("\n" + engine.start_session(name, followers, eng, budget))
    print("\n(Type 'quit' to exit, or just press Enter to simulate a pause)")
    
    while True:
        try:
            user_input = input("\nInfluencer says: ")
        except EOFError:
            break
            
        if user_input.lower() in ["quit", "exit"]:
            print("Exiting...")
            break
            
        if not user_input.strip():
            print("(Waiting for influencer response...)")
            continue
            
        print("Bot is thinking...")
        try:
            response = engine.process_message(user_input)
            
            print(f"\n[Internal Thought]: {response.internal_thought}")
            print(f"[Bot Message]: {response.message_to_influencer}")
            
            if response.suggested_offer:
                 print(f"[OFFER DETECTED]: ${response.suggested_offer}")
                 
            if response.is_deal_reached:
                print("\n*** PENDING DEAL REACHED! (Bot flagged success) ***")
                break
            if response.is_deal_lost:
                print("\n*** NEGOTIATION ENDED (Bot flagged failure) ***")
                break
        except Exception as e:
            print(f"Error processing message: {e}")

if __name__ == "__main__":
    main()
