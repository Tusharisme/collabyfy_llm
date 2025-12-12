# Negotiation Chatbot Tool

This tool provides an autonomous negotiation agent capable of engaging with influencers to reach a deal within a specified budget. It uses Google's Gemini LLM to generate context-aware, persuasive, and strategy-driven responses.

## Features
- **Intelligent Negotiation**: Uses a "Collaborative" strategy to find mutual ground.
- **Budget Guardrails**: Automatically caps offers at the maximum budget.
- **Deal Detection**: Recognizes when an agreement has been reached or if the negotiation has failed.
- **Structured Output**: Returns internal reasoning and specific offer amounts alongside the message.

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
Run the CLI to test the chatbot interactively:
```bash
python main.py
```
You will be prompted to enter:
- Influencer Name
- Follower Count
- Engagement Rate
- Max Budget

Then you can simulate the influencer's responses by typing in the terminal.

## Integration Guide (Collabyfy App)

To integrate this tool into the main Collabyfy application (Next.js/Node.js), follow this architectural recommendation.

### 1. "Smart Assistant" Workflow
The chatbot should act as an agent within your Direct Messaging (DM) system.
- **Auto-Negotiate Toggle**: Add a checkbox `[x] Enable AI Negotiation` when creating a Campaign.
- **Trigger**: When an influencer sends a proposal (and the price > budget), the bot automatically replies.

### 2. UI/UX Recommendations
- **Transparency**: Label bot messages (e.g., "⚡ AI Assistant") so influencers know they are initially negotiating with a system.
- **Manual Override**: Allow the brand user to take over the chat at any time.

### 3. Technical Implementation
**Webhooks & API**:
Instead of running `main.py` manually, wrap `engine.py` in a lightweight API (e.g., FastAPI) or invoke it via a worker process.

1.  **Webhook Event**: When a message arrives in your main app:
    ```javascript
    // Next.js Backend (Pseudo-code)
    if (campaign.enable_ai_negotiation && message.offer > campaign.budget) {
        // Send payload to Python Bot Service
        await callNegotiationBot({
            history: chatHistory, 
            context: campaignDetails
        });
    }
    ```

2.  **State Management**:
    - **Persist History**: Store the negotiation history (`models.py` > `ChatSession`) in your main database (PostgreSQL/MongoDB).
    - **Context Awareness**: Pass the full history to the bot on every turn so it remains stateless and scalable.

3.  **Deal Success**:
    - Listen for `is_deal_reached: true` in the bot's response.
    - Automatically update the proposal status to **"Pending Approval"**.
