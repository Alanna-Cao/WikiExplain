from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import requests

load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

WIKI_API_ENDPOINT = "https://en.wikipedia.org/w/api.php"

# Get the full plain text of a Wikipedia article
def fetch_article_content(title):
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'extracts',
        'titles': title,
        'explaintext': True
    }
    response = requests.get(WIKI_API_ENDPOINT, params=params).json()
    pages = response['query']['pages']
    page = next(iter(pages.values()))
    return page.get('extract', '')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    title = data['title']
    detail_level = data['detail']  # 'short', 'medium', 'long'

    article_text = fetch_article_content(title)
    if not article_text:
        return jsonify({'error': 'Article not found'}), 404

    prompt = f"""
    You are an assistant that provides layered summaries of Wikipedia articles. Based on the requested level of detail, summarize the article titled '{title}'.
    - If the user asks for 'short', provide 1–2 sentence overview.
    - If 'medium', give 4–6 bullet points on major themes.
    - If 'long', provide a detailed multi-paragraph summary, broken into sections.
    
    Article:
    {article_text[:4000]}

    Summary ({detail_level}):
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    summary = response.choices[0].message.content

    return jsonify({ 'summary': summary })

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)