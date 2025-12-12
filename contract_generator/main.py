import argparse
import sys
import os
import json
from datetime import date

# Add parent path to allow imports if running primarily from here
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generator import ContractGenerator
from renderer import ContractPDF
from models import ContractRequest, Party, Deliverable, PaymentTerms

def main():
    parser = argparse.ArgumentParser(description="Automated Contract Generator")
    parser.add_argument("--output", default="contract.pdf", help="Output filename")
    args = parser.parse_args()
    
    # Mock Data for demonstration
    req = ContractRequest(
        brand=Party(name="NextGen Tech", email="legal@nextgen.com", role="Brand"),
        influencer=Party(name="Sarah Creator", minimize_details=False, email="sarah@content.com", role="Influencer"),
        effective_date=str(date.today()),
        campaign_name="Summer Launch 2025",
        deliverables=[
            Deliverable(description="High energy unboxing video", platform="TikTok", due_date="2025-06-01"),
            Deliverable(description="Lifestyle photo with product", platform="Instagram", due_date="2025-06-05", format="Post"),
            Deliverable(description="Follow-up review after 1 week usage", platform="YouTube", due_date="2025-06-15")
        ],
        payment_terms=PaymentTerms(
            total_amount=5000.00,
            currency="USD",
            schedule="50% upon signing, 50% upon completion of all deliverables."
        ),
        exclusivity_clause="Influencer agrees not to promote competitor tech brands for 30 days post-campaign."
    )
    
    print("Initializing Generator...")
    try:
        generator = ContractGenerator()
        renderer = ContractPDF()
        
        print("Generating contract content (AI + Template)...")
        content = generator.generate(req)
        
        print(f"Rendering PDF to {args.output}...")
        renderer.render(content, args.output)
        print("Done!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
