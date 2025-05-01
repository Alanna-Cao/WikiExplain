explicilty say that no open source code was used, all written by me (Please include a README file that specifies what open-source code you imported (if any), what changes you made, and what new code you implemented. (If you built your application based on any open-source initial code, we expect you make nontrivial changes to the code.) 
)

# WikiExplain: Interactive Wikipedia Summarizer

**WikiExplain** is a lightweight web app that helps users explore Wikipedia articles through customizable, AI-generated summaries. Built for the Spring 2025 HAII final project, it emphasizes human-centered interaction and explainability.

## Features

- Adjust **length** and **technicality** of summaries with sliders
- Breaks articles into **section-based summaries**
- Supports **highlight-to-clarify** AI probing on phrase or sentence level granularity
- Includes a **regenerate** button for rewrites
- Uses **GPT-4o** in zero-shot mode (no fine-tuning)
- Floating Table of Contents and collapsible sections

## Tech Stack

- **Backend**: Flask + OpenAI API
- **Frontend**: Tailwind CSS + custom JavaScript
- **Data**: Wikipedia articles via Wikipedia API

## Concepts from HAII

- Prompt Engineering to guide tone, verbosity, and format
- Human-AI Interaction Guidelines:
  - #7 & #9 – Fast recovery via Regenerate / Clarify
  - #15 – Sentence-level feedback and explainability
- Designed for AI failure and user control

## Pilot User Study

Feedback from 4 users led to:
- Clearer technicality sliders
- Softer prompts for more useful conciseness
- Link to original article added

Overall, it could be seen that users especially valued the **agency and control** over AI-generated responses.

## Setup

1. Clone the repo
2. Add your `.env` with OpenAI key:

   ```
   OPENAI_API_KEY=your-api-key
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the app with:
   ```
   python app.py
   ```
5. Once running, Flask will display a local development URL — typically something like:
   "Running on http://127.0.0.1:5000/". Open this address in your browser to use the app
   
   (Note: it may also appear as `http://localhost:5000`, or a different port like `:8000` depending on your setup.)