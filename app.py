from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import re
import requests

load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

WIKI_API_ENDPOINT = "https://en.wikipedia.org/w/api.php"

def fetch_article_content(title):
    search_params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': title
    }
    search_response = requests.get(WIKI_API_ENDPOINT, params=search_params).json()
    search_results = search_response.get('query', {}).get('search', [])
    if not search_results:
        return ''
    best_match_title = search_results[0]['title']

    extract_params = {
        'action': 'query',
        'format': 'json',
        'prop': 'extracts',
        'titles': best_match_title,
        'explaintext': True
    }
    extract_response = requests.get(WIKI_API_ENDPOINT, params=extract_params).json()
    pages = extract_response['query']['pages']
    page = next(iter(pages.values()))
    return page.get('extract', '')

def strip_markdown(text):
    patterns = [
        r'\*\*(.*?)\*\*', r'\*(.*?)\*', r'_([^_]+)_', r'`([^`]+)`', r'\[([^\]]+)\]\([^\)]+\)'
    ]
    for pattern in patterns:
        text = re.sub(pattern, r'\1', text)
    return text

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    title = data['title'].strip()
    length_level = int(data.get('length', 50))  # 0–100: concise → detailed
    technical_level = int(data.get('technical', 50))  # 0–100: less technical → more technical

    article_text = fetch_article_content(title)
    if not article_text:
        return jsonify({'error': 'Article not found'}), 404

    if technical_level < 25:
        tech_note = "Use extremely simple language and avoid any jargon."
    elif technical_level < 50:
        tech_note = "Explain using beginner-friendly language and only basic terms."
    elif technical_level < 75:
        tech_note = "Use moderately advanced language with some technical vocabulary."
    else:
        tech_note = "Use technical terms and expert-level detail assuming domain familiarity."

    if length_level < 25:
        length_note = "Write a one-sentence ultra-brief summary per section."
    elif length_level < 50:
        length_note = "Summarize briefly with 1–2 short sentences per section."
    elif length_level < 75:
        length_note = "Write a 3–4 sentence paragraph per section with moderate detail."
    else:
        length_note = "Write long-form paragraph summaries with extensive depth and elaboration."

    prompt = f"""
    You are an AI assistant summarizing Wikipedia articles for general audiences.

    Instructions:
    - Summarize the article titled \"{title}\".
    - Use bold section headings (e.g., **Gameplay Mechanics**), followed by paragraph-style summaries.
    - Do not use bullet points or markdown. Return plain text only.
    - Style: {tech_note}
    - Length: {length_note}

    Wikipedia Article:
    {article_text[:4000]}

    Response:
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    summary = strip_markdown(response.choices[0].message.content)
    return jsonify({'summary': summary})

@app.route('/clarify', methods=['POST'])
def clarify():
    print("clarify endpoint hit")
    data = request.json
    selected_text = data['text'].strip()
    print("selected text: ", selected_text)
    
    if not selected_text or len(selected_text.split()) < 2:
        return jsonify({'clarification': "Sorry, couldn't find text to clarify."})

    prompt = f"""
    Explain the following sentence clearly and simply. Do not include greetings or acknowledgements like 'Certainly' — just give the explanation directly.

    Sentence:
    \"{selected_text}\"
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    clarification = strip_markdown(response.choices[0].message.content)
    return jsonify({'clarification': clarification})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)