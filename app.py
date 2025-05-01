"""
This Flask application provides two main functionalities:
1. Summarizing Wikipedia articles based on user input.
2. Clarifying specific sentences from the summarized text.
The application uses OpenAI's GPT-4 model to generate summaries and clarifications.
"""

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

"""
Fetches the content of a Wikipedia article based on the title.
If the article is not found, it returns an empty string and an empty URL.
Args:
    title (str): The title of the Wikipedia article to fetch.
Returns:
    tuple: A tuple containing the article text and the URL of the article.
"""
def fetch_article_content(title):
    # Search for the article using the title
    search_params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': title
    }
    search_response = requests.get(WIKI_API_ENDPOINT, params=search_params).json()
    search_results = search_response.get('query', {}).get('search', [])
    if not search_results:
        return '', ''

    best_match_title = search_results[0]['title']
    article_url = f"https://en.wikipedia.org/wiki/{best_match_title.replace(' ', '_')}"

    # Fetch the article content using the best match title
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
    return page.get('extract', ''), article_url

"""
Helper function that strips markdown formatting from the text.
Args:
    text (str): The text to be stripped of markdown.
Returns:
    str: The text without markdown formatting.
"""
def strip_markdown(text):
    patterns = [
        r'\*\*(.*?)\*\*', r'\*(.*?)\*', r'_([^_]+)_', r'`([^`]+)`', r'\[([^\]]+)\]\([^\)]+\)'
    ]
    for pattern in patterns:
        text = re.sub(pattern, r'\1', text)
    return text

"""
Flask route to handle the summarization of Wikipedia articles.
It accepts a POST request with JSON data containing the article title, length level, and technical level.
The route fetches the article content, generates a summary using OpenAI's GPT-4 model, and returns the summary along with the article URL.
"""
@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    title = data['title'].strip()
    length_level = int(data.get('length', 50))  # 0–100: concise → detailed
    technical_level = int(data.get('technical', 50))  # 0–100: less technical → more technical

    article_text, article_url = fetch_article_content(title)
    if not article_text:
        return jsonify({'error': 'Article not found'}), 404

    if technical_level < 25:
        tech_note = "Use extremely simple language and avoid any technical jargon."
    elif technical_level < 50:
        tech_note = "Explain using beginner-friendly technical language and only basic terms."
    elif technical_level < 75:
        tech_note = "Use moderately advanced language with some technical vocabulary."
    else:
        tech_note = "Use technical terms and expert-level detail assuming high domain familiarity."

    if length_level < 25:
        length_note = "Write a one-sentence brief summary per section."
    elif length_level < 50:
        length_note = "Summarize briefly with 1-2 short sentences per section."
    elif length_level < 75:
        length_note = "Write a 3-4 sentence paragraph per section with moderate detail."
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
    return jsonify({'summary': summary, 'url': article_url})

"""
Flask route to handle the clarification of selected text.
It accepts a POST request with JSON data containing the selected text.
The route generates a clarification using OpenAI's GPT-4 model and returns the clarification.
"""
@app.route('/clarify', methods=['POST'])
def clarify():
    data = request.json
    selected_text = data['text'].strip()
    
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

"""
Flask route to render the main index page.
It serves the HTML template for the application.
"""
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)