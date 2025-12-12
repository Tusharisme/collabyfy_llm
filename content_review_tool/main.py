import argparse
import sys
import os

# Add parent dir to path to allow importing from local dir
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analyzer import ContentAnalyzer

def main():
    parser = argparse.ArgumentParser(description="AI Content Review Tool")
    parser.add_argument("--image", required=True, help="Path to the image file")
    parser.add_argument("--caption", required=True, help="Caption text")
    
    args = parser.parse_args()
    
    print("Initializing Analyzer...")
    try:
        analyzer = ContentAnalyzer()
        
        print(f"Analyzing content...\nImage: {args.image}\nCaption: {args.caption}")
        result = analyzer.analyze(args.image, args.caption)
        
        print("\n" + "="*40)
        print(f" OVERALL SCORE: {result.overall_score}/100")
        print("="*40)
        print(f"SUMMARY: {result.summary}\n")
        
        print(f"METRICS:")
        print(f"- Tone: {result.metrics.tone_score}")
        print(f"- Image Quality: {result.metrics.image_quality_score}")
        print(f"- Relevance: {result.metrics.caption_relevance_score}")
        print(f"- Compliance: {result.metrics.compliance_score}\n")
        
        print("SUGGESTIONS:")
        for i, sugg in enumerate(result.suggestions, 1):
            print(f"{i}. [{sugg.category}] {sugg.feedback}")
            print(f"   -> TIP: {sugg.actionable_tip}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
