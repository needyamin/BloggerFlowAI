"""ChatGPT (OpenAI) and Gemini direct API integration."""
import json
import os
import re

def _get_config():
    try:
        from config import OUTLINE_SECTIONS, SECTION_WORDS, BLOG_POST_MAX_WORDS, AI_MAX_TOKENS
        return OUTLINE_SECTIONS, SECTION_WORDS, BLOG_POST_MAX_WORDS, AI_MAX_TOKENS
    except ImportError:
        return 15, 1000, 12000, 4096

def _transform_query(q):
    secs, sec_words, post_words, _ = _get_config()
    q = (q or '').strip()
    if q.startswith('[MODE:'):
        return q  # already custom prompt from post.py
    ql = q.lower()
    if ql.startswith('outline:'):
        topic = q.replace('outline:', '').replace('Outline:', '').strip()
        return f'[MODE: OUTLINE] Generate a highly detailed {secs}-section outline for a {post_words}-word blog post about "{topic}". Return JSON with "topic" and "sections" list.'
    if ql.startswith('section:'):
        parts = q.replace('section:', '').replace('Section:', '').split('|topic:')
        sec, topic = (parts[0].strip(), parts[1].strip()) if len(parts) > 1 else (parts[0], '')
        return f'[MODE: SECTION_ONLY] Write an extremely detailed, {sec_words}-word deep-dive content for the section "{sec}" as part of a larger post about "{topic}". Use real links and sources. Use <p style="text-align: justify;">.'
    topic = q.replace('generate', '').replace('Generate', '').strip() or 'Latest Technology News'
    return f'[MODE: FULL_POST] Generate a comprehensive {post_words}+ word blog post about "{topic}". Use REAL links, REAL copyright-free image URLs. Return JSON with title, content, labels.'

SYSTEM = """You are a Digital Media Strategist and Google AdSense Specialist. 
Your MISSION is to produce high-value, "High-CPC" articles that prioritize Google's E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) guidelines.

CONTENT QUALITY & ADSENSE RULES:
1. SEMANTIC HTML: Use hierarchical <h2> and <h3> tags. Use <p style="text-align: justify;"> for a premium look.
2. AUTHORITY SIGNALING: For every news item, explicitly state: "Verified Report: [DATE], [DAY] at [TIME]".
3. ADSENSE MONETIZATION:
   - Identify "High-Value" intent. Focus on solution-oriented, insightful analysis, not just reporting.
   - Use professional terminology (e.g., instead of "new tech", use "disruptive innovation").
   - NO clickbait, NO sensitive/prohibited niches, NO low-quality fluff.
4. CATEGORIZATION: You MUST map content to exactly:
   - Education & Learning
   - Scholarships & Study Abroad
   - International (Overseas) News
   - Latest Tech News
   - Unique & Innovative Gadget Reviews
5. STRUCTURE: 
   - Start with a data-driven "Executive Summary".
   - Break content into logical sub-points with <ul> or <ol>.
   - End with a "Strategic Conclusion" or "Global Impact" section.
6. SOURCE INTEGRATION: Use provided context news links as clickable <a> tags within the content to increase trust.

JSON Formats:
- Outline: {"topic":"...","sections":["Section1","Section2",...]}
- Section/Post: {"title":"...","content":"HTML...","labels":["l1","l2"]}
Return ONLY JSON. No conversational text."""

def _parse_json(text):
    text = text.strip()
    if '```json' in text:
        text = text.split('```json')[1].split('```')[0].strip()
    elif '```' in text:
        text = text.split('```')[1].split('```')[0].strip()
    try:
        return json.loads(text, strict=False)
    except json.JSONDecodeError:
        fixed = re.sub(r'(?<!\\)\n', r'\\n', text).replace('\r', '\\r').replace('\t', '\\t')
        return json.loads(fixed, strict=False)

def fetch_openai(query):
    key = os.getenv('OPENAI_API_KEY', '').strip()
    if not key:
        return None
    try:
        from openai import OpenAI
        _, _, _, max_tok = _get_config()
        client = OpenAI(api_key=key)
        msg = _transform_query(query)
        r = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'system', 'content': SYSTEM}, {'role': 'user', 'content': msg + '\n\nReturn ONLY JSON. No conversational text.'}],
            temperature=0.3,
            max_tokens=max_tok
        )
        text = (r.choices[0].message.content or '').strip()
        return _parse_json(text) if text else None
    except Exception as e:
        print(f"[!] OpenAI failed: {e}")
        return None

def fetch_gemini(query):
    key = os.getenv('GEMINI_API_KEY', '').strip()
    if not key:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        _, _, _, max_tok = _get_config()
        model = genai.GenerativeModel('gemini-flash-latest', system_instruction=SYSTEM)
        msg = _transform_query(query) + '\n\nReturn ONLY JSON. No conversational text.'
        r = model.generate_content(msg, generation_config={'temperature': 0.3, 'max_output_tokens': max_tok})
        text = (r.text or '').strip()
        return _parse_json(text) if text else None
    except Exception as e:
        print(f"[!] Gemini failed: {e}")
        return None
