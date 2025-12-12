# Smart Brief Generator

This tool uses **Gemini 2.5 Flash** to instantly generate professional campaign brief PDFs from short brand prompts. It is designed to be **stateless and scalable**, utilizing **FPDF2** for fast, high-concurrency PDF rendering.

## Features
- **Magic Autofill**: Turns "Coffee brand launch" into a full 2-page brief with Overview, Audience, deliverables, etc.
- **PDF Export**: Generates a standardized, clean PDF ready for download.
- **Stateless**: Can be deployed on serverless functions (like AWS Lambda) as it requires no browser dependency.

## Setup
1.  **Prerequisites**: Python 3.9+
2.  **Installation**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Environment Variables**:
    Create a `.env` file in this directory:
    ```ini
    API_KEY=your_gemini_api_key_here
    ```

## Usage
Run the CLI to generate a brief:
```bash
python main.py --brand "Your Brand" --topic "Campaign Topic" --focus "Key Message"
```

Example:
```bash
python main.py --brand "Morning Brew" --topic "Summer Launch" --focus "Energy"
```
This will create `campaign_brief.pdf` in the current directory.

## Integration Guide (Collabyfy App)

To use this in your Campaign Creation flow:

1.  **API Endpoint**: Wrap `main.py`'s logic in a FastAPI endpoint.
    - Input: JSON `{ "topic": "..." }`
    - Output: Streaming response (PDF bytes).
2.  **Frontend**: Add a "Generate with AI" button next to the brief description field.
3.  **Performance**: Since `FPDF2` is lightweight, you can run this synchronously or in a simple thread pool; no heavy queue is required for low traffic volumes.
