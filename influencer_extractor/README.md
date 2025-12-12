# Influencer Criteria Extractor

This tool uses Generative AI to analyze natural language campaign briefs and extract strict, structured JSON criteria for influencer search.

## Features
- **Zero-Hallucination Extraction**: Strictly returns `null` for missing information (e.g., if "Gender" isn't mentioned, it returns `null` instead of guessing).
- **Structured JSON**: Outputs a standardized schema ready for database queries or filtering algorithms.
- **Robust Parsing**: Handles markdown formatting and potential API response variations.

## Setup
1.  **Prerequisites**: Python 3.9+
2.  **Installation**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Ensure `google-generativeai` and `python-dotenv` are in requirements.txt)*
3.  **Environment Variables**:
    Create a `.env` file in this directory:
    ```ini
    API_KEY=your_gemini_api_key_here
    ```

## Usage
Run the script to see an example extraction:
```bash
python main.py
```
To use it in your code, import the function:
```python
from main import extract_strict_criteria

brief = "Looking for beauty influencers in Mumbai with >50k followers."
criteria = extract_strict_criteria(brief)
print(criteria)
```

## Integration Guide (Collabyfy App)
Use this tool in your **Campaign Creation** flow.

1.  **Input**: Allow Brands to describe their requirements in plain text (e.g., "I need fashion bloggers in Delhi").
2.  **Process**: Call `extract_strict_criteria` to convert this text into filter parameters.
3.  **Action**: Use the resulting JSON to pre-fill your Search Filters or query your Influencer Database directly.
