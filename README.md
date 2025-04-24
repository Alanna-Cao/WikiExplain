# WikiReframe: What Just Changed?

A lightweight AI-powered tool to track the most recent changes to any Wikipedia article. It helps you understand not just what changed — but how the framing, tone, and emphasis might have shifted.

## Features
- Automatically compares the **latest two revisions** of any Wikipedia article
- Uses **GPT-4o** to summarize tone and framing changes
- Displays a raw unified diff alongside the AI-generated summary

## Setup
1. Clone this repo
2. Create a `.env` file and add your API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```
3. Run `pip install -r requirements.txt`
4. Run the app: `python app.py`
5. Open [http://localhost:5000](http://localhost:5000) in your browser

## File Overview
- `app.py` – Flask backend fetching latest Wikipedia revisions and summarizing them
- `templates/index.html` – Simple browser UI
- `.env` – Store your OpenAI API key (excluded from git)

## Example Use Case
> “What just changed in the article on *Climate change*?”

## License
MIT