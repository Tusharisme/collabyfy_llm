import argparse
import sys
import os

# Add parent path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generator import BriefContentGenerator
from renderer import PDFRenderer
from models import BriefRequest, BriefData

def main():
    parser = argparse.ArgumentParser(description="Smart Campaign Brief Generator")
    parser.add_argument("--brand", help="Brand name")
    parser.add_argument("--topic", help="Campaign topic")
    parser.add_argument("--audience", help="Target audience")
    parser.add_argument("--focus", help="Key message focus")
    parser.add_argument("--output", default="campaign_brief.pdf", help="Output PDF filename")
    parser.add_argument("--save-json", help="Save the generated content to a JSON file for editing")
    parser.add_argument("--from-json", help="Render PDF directly from a JSON file (skips AI generation)")
    
    args = parser.parse_args()
    
    print("Initializing Generator...")
    try:
        generator = BriefContentGenerator()
        renderer = PDFRenderer()
        
        data = None

        if args.from_json:
            print(f"Loading data from {args.from_json}...")
            with open(args.from_json, 'r') as f:
                import json
                raw_data = json.load(f)
                data = BriefData(**raw_data)
        else:
            if not args.brand or not args.topic:
                print("Error: --brand and --topic are required unless using --from-json")
                sys.exit(1)
                
            req = BriefRequest(
                brand_name=args.brand,
                campaign_topic=args.topic,
                target_audience=args.audience,
                key_message_focus=args.focus
            )
            
            print(f"Generating content for '{args.topic}'...")
            data = generator.generate(req)
            print("Content generated successfully.")
            
            if args.save_json:
                print(f"Saving draft to {args.save_json}...")
                with open(args.save_json, 'w') as f:
                    f.write(data.model_dump_json(indent=2))
        
        print(f"Rendering PDF to {args.output}...")
        renderer.render(data, args.output)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
