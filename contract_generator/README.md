# Automated Contract Generator

A production-ready AI tool for generating professional influencer marketing agreements.
This tool uses a **Hybrid Approach**:
1.  **AI (Gemini)**: Drafts the variable "Schedule A" (Services) and "Schedule B" (Payment) based on campaign data.
2.  **Standard Template**: Uses hardcoded, legally-sound boilerplate for the main contract terms to ensure safety and compliance.
3.  **PDF Engine**: Generates clean, e-sign ready PDFs using `fpdf2`.

## Features
- **Structured Inputs**: Accepts rigorous data via Pydantic models.
- **Smart Drafting**: Converts loose deliverable lists into professional legal language.
- **E-Sign Ready**: Embeds invisible "Anchor Tags" (`/s1/`, `/s2/`) for DocuSign/HelloSign auto-placement.
- **Stateless & Fast**: Generates PDFs in <2 seconds.

## Setup
1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Set up API Key in `.env`:
    ```
    API_KEY="your_gemini_api_key"
    ```

## Usage (CLI)
Run the generator with mock data:
```bash
python main.py --output my_contract.pdf
```

## Integration Guide
To integrate this into the main Collabyfy app:

1.  **Backend Endpoint**: Create a route (e.g., `POST /api/contracts/generate`).
2.  **Request Body**:
    ```json
    {
      "brand": {"name": "...", "email": "...", "role": "Brand"},
      "influencer": {"name": "...", "email": "...", "role": "Influencer"},
      "deliverables": [...],
      "payment_terms": {...}
    }
    ```
3.  **Logic**:
    ```python
    from contract_generator.generator import ContractGenerator
    from contract_generator.renderer import ContractPDF
    from contract_generator.models import ContractRequest

    # inside your view/controller
    req = ContractRequest(**request.json)
    gen = ContractGenerator()
    content = gen.generate(req)
    
    renderer = ContractPDF()
    renderer.render(content, "/path/to/temp/contract.pdf")
    # Return file to user
    ```
