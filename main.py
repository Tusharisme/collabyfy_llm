import google.generativeai as genai
import json
import os
import dotenv

dotenv.load_dotenv()
# --- Configuration ---
# Replace "YOUR_API_KEY" with your actual key.
API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)
# --- The NEW, STRICT Prompt Template ---
# (This part remains the same as before)
PROMPT_TEMPLATE_STRICT = """
You are a precise data extraction agent. Your task is to analyze the following campaign brief and extract information into a JSON object.

**Instructions:**
1.  Read the campaign brief very carefully.
2.  Populate the JSON structure provided below using ONLY information that is **explicitly stated** in the brief.
3.  **CRITICAL:** If a value for a specific field cannot be found in the text, you MUST use `null` for that field. Do not guess, infer, or invent any information.
4.  Your final output must be ONLY the JSON object, with no other text or explanations before or after it.

**JSON Structure to Populate:**
{{
    "Influencer": {{
        "Networks": [],
        "Category/Keyword": [],
        "Location": [],          // e.g., ["Mumbai", "India"]
        "Followers": null,       // e.g., "50k-250k"
        "Gender": null,
        "Language": [],          // e.g., ["English", "Hindi"]
        "Hashtags": [],
        "Mentions": [],
        "Cost per Publication": null,
        "Verified": null,
        "Lookalike": [],
        "Audience": {{
            "AQS": null,
            "Age Range": null,
            "Location": [],
            "Interest": [],
            "Language": [],
            "Gender": null,
            "Authenticity": null
        }},
        "Performance": {{
            "Engagement %": null,
            "Days since last post": null,
            "Estimated Reach": null,
            "Likes per Post": null,
            "Comments per Post": null
        }},
        "Exclusion": {{
            "Exclude Category/Keyword": [],
            "Exclude Location": [],
            "Exclude Hashtags": [],
            "Exclude Mentions": [],
            "Exclude Brands": [],
            "Exclude Creators": []
        }}
    }}
}}

**Campaign Brief:**
---
{campaign_brief}
---
"""


def extract_strict_criteria(campaign_brief: str) -> dict:
    """
    Uses the Gemini API to STRICTLY extract influencer search criteria from a brief.
    This version includes a robust method for accessing the response text.
    """
    # This check now correctly looks for the placeholder text.
    if not API_KEY:
        return {
            "error": "API key not configured. Please replace 'YOUR_API_KEY' in the script."
        }

    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        full_prompt = PROMPT_TEMPLATE_STRICT.format(campaign_brief=campaign_brief)
        response = model.generate_content(full_prompt)

        # Robustly access the response text
        if not response.parts:
            # Handle cases where the response might be blocked or empty
            feedback = response.prompt_feedback
            return {
                "error": "The model did not return any content.",
                "prompt_feedback": str(feedback),
            }

        model_output_text = response.parts[0].text

        cleaned_response = (
            model_output_text.strip().replace("```json", "").replace("```", "")
        )
        json_output = json.loads(cleaned_response)
        return json_output

    except json.JSONDecodeError:
        raw_text = (
            response.parts[0].text if response.parts else "No text found in response"
        )
        return {
            "error": "Failed to parse the model's response as JSON.",
            "raw_response": raw_text,
        }
    except Exception as e:
        return {
            "error": f"An unexpected error occurred: {type(e).__name__}",
            "details": str(e),
        }


# --- Example Usage ---
if __name__ == "__main__":
    user_input = """
    We are launching a new campaign called “Fresh Start, Fresh You” to introduce our latest Herbal Skincare Range.
    Our main audience is young adults between 18–35 who are health-conscious, eco-friendly, and active on social media.
    The campaign will launch with ads across Instagram, YouTube, TikTok, and Facebook. 
    To keep people engaged, we’ll run a hashtag challenge called #FreshStartChallenge. 
    The overall budget for three months is around ₹20 lakhs.
    We want to collaborate with influencers who have 90k plus followers and speak English or Hindi.
    """

    result = extract_strict_criteria(user_input)
    print(json.dumps(result, indent=2))
