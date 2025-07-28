# WikiExplain: Interactive Wikipedia Article Summarizer

WikiExplain is a full-stack web application that dynamically summarizes Wikipedia articles using GPT-4o, offering user-controlled summarization based on length and complexity. The tool emphasizes fine-grained user interaction, fast feedback loops, and explainability — useful for both casual exploration and deeper learning.

Originally built as a final project for the [Human AI Interaction course](https://www.hcii.cmu.edu/course/human-ai-interaction) at Carnegie Mellon University's Human-Computer Interaction Institute, it now serves as a standalone demo of custom LLM prompting, frontend–backend integration, and human-centered AI design

## Features
- **Real-time summarization controls:** Adjustable sliders for summary length and technicality, dynamically modifying prompt parameters sent to GPT-4o.
- **Section-aware output:** Wikipedia content is split by top-level headings, with summaries generated and displayed per section.
- **Granular AI probing:** Users can highlight any phrase or sentence to get a local explanation or simplification via contextual prompting.
- **Content regeneration:** On-demand rewrite button enables fast recovery from off-target generations.
- **User-friendly UI:** Floating Table of Contents, collapsible sections, and clean, responsive design.

## Tech Stack
- **Backend**: Python + Flask (RESTful API server, prompt orchestration)
- **LLM**: OpenAI GPT-4o (accessed via OpenAI API)
- **Frontend**: Tailwind CSS, JavaScript (DOM manipulation, UI/UX logic)
- **Data Source:** Wikipedia API (live article fetches)

## Code Origin
No open-source code was used in this project. All frontend and backend logic — including Flask server logic, API querying, prompt engineering, and JavaScript interactions — were written entirely by me from scratch.

## Concepts from HAII Course Content
- Prompt Engineering to guide tone, verbosity, and format
- Human-AI Interaction Guidelines:
  - #7 & #9 – Fast recovery via Regenerate / Clarify
  - #15 – Granular (sentence and phrase-level) feedback, and explainability
- Designed for AI failure and user control

## User Feedback & Iteration
Pilot tested with 4 users (non-technical and technical). Resulting changes:
- Improved UI for technicality controls (clearer labels and effects)
- Refined prompts for better summarization consistency
- Added original article link and clarify-on-highlight for better user trust and control

## Setup
```
# 1. Clone the repo
git clone https://github.com/your-username/WikiExplain.git
cd WikiExplain

# 2. Set up environment variables
echo "OPENAI_API_KEY=your-api-key" > .env

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Flask app
python app.py
```
App runs on http://127.0.0.1:5000 by default.

