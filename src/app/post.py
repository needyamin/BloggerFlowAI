import os
import json
import re
import pickle
import random
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from config import (
    CREDENTIALS_FILE, TOKEN_FILE, BLOGGER_BLOG_ID,
    OPENAI_API_KEY, GEMINI_API_KEY, TOPIC, TOPICS,
    BLOG_POST_MIN_WORDS, BLOG_POST_MAX_WORDS, POST_TITLE_MAX_CHARS, FORCE_POST, OUTLINE_SECTIONS,
    SECTION_WORDS, LOG_VERBOSE, MSG_START, MSG_PHASE1, MSG_OUTLINE_READY, MSG_PHASE2_HEADER,
    MSG_PHASE2_SECTION, MSG_COMPLETE, FIRST_SECTION_NAME
)
from models.remote_agent import fetch_openai, fetch_gemini

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/blogger']

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES, redirect_uri='http://127.0.0.1:8081/'
            )
            creds = flow.run_local_server(port=8081, host='127.0.0.1')
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def _word_count(html):
    return len(re.sub(r"<[^>]+>", " ", html or "").split())

def _fetch_ai(query):
    if OPENAI_API_KEY:
        r = fetch_openai(query)
        if r:
            return r
    if GEMINI_API_KEY:
        r = fetch_gemini(query)
        if r:
            return r
    print(f"[!] All APIs failed for query '{query[:50]}...'")
    return None

def _log(msg, **kw):
    if LOG_VERBOSE:
        print(msg.format(**kw) if kw else msg)

def generate_ai_content(topic=None, context_news=None):
    selected_topic = topic or random.choice(TOPICS)
    
    # Build context string if news items are provided
    context_str = ""
    if context_news:
        context_str = "\n\nUSE THE FOLLOWING REAL-TIME NEWS AS YOUR PRIMARY SOURCE AND EVIDENCE:\n"
        for idx, item in enumerate(context_news[:5], 1): # Use top 5 news items
            context_str += f"[{idx}] Source: {item.get('source')} | Title: {item.get('title')} | Content Snippet: {item.get('content')[:500]} | Link: {item.get('link')}\n"
    
    _log(MSG_START, topic=selected_topic)
    _log(MSG_PHASE1, n=OUTLINE_SECTIONS)
    
    outline_query = (
        f"[MODE: OUTLINE] Generate EXACTLY {OUTLINE_SECTIONS} sections for a {BLOG_POST_MAX_WORDS}-word, high-level, authoritative blog post about \"{selected_topic}\". "
        f"IMPORTANT: You MUST focus ONLY on news from the year 2026. For every news item or event mentioned, clearly state the exact DATE, DAY, and TIME it occurred. "
        f"ASSIGN each news item to exactly one of these categories: Education & Learning, Scholarships & Study Abroad, International (Overseas) News, Latest Tech News, Unique & Innovative Gadget Reviews. "
        f"Return JSON with \"topic\" and \"sections\" array of exactly {OUTLINE_SECTIONS} section titles. No more, no less.{context_str}"
    )
    outline_data = _fetch_ai(outline_query)
    if not outline_data or 'sections' not in outline_data:
        _log("[!] Failed to get outline. Using fallback single-shot generation.")
        return _fetch_ai(f"generate {selected_topic}") or {'title': selected_topic, 'content': '<p>Content generation failed.</p>', 'labels': ['error']}
    sections = outline_data['sections'][:OUTLINE_SECTIONS]
    _log(MSG_OUTLINE_READY, n=len(sections))
    full_html = ""
    _log(MSG_PHASE2_HEADER)
    header_query = (
        f"[MODE: SECTION_ONLY] Write an extremely detailed, {SECTION_WORDS}-word deep-dive content for the section \"{FIRST_SECTION_NAME}\" as part of a larger, authoritative post about \"{selected_topic}\". "
        f"MANDATORY: Use ONLY 2026 news. Mention DATE, DAY, and TIME for events. "
        f"Categorize into: Education & Learning, Scholarships & Study Abroad, International (Overseas) News, Latest Tech News, Unique & Innovative Gadget Reviews. "
        f"Use real links and sources. Use <p style=\"text-align: justify;\">.{context_str}"
    )
    header_data = _fetch_ai(header_query)
    if header_data:
        full_html += header_data.get('content', '')
        final_labels = header_data.get('labels', [])
        final_title = header_data.get('title', f"The Ultimate Guide to {selected_topic}")
    else:
        final_labels = ["education", selected_topic.lower()]
        final_title = f"The Definitive Guide to {selected_topic}"
    for i, section in enumerate(sections[1:], 2):
        _log(MSG_PHASE2_SECTION, i=i, total=len(sections), section=section)
        sec_query = (
            f"[MODE: SECTION_ONLY] Write an extremely detailed, {SECTION_WORDS}-word deep-dive content for the section \"{section}\" as part of a larger, authoritative post about \"{selected_topic}\". "
            f"MANDATORY: Use ONLY 2026 news. Mention DATE, DAY, and TIME for events. "
            f"Categorize into: Education & Learning, Scholarships & Study Abroad, International (Overseas) News, Latest Tech News, Unique & Innovative Gadget Reviews. "
            f"Use real links and sources. Use <p style=\"text-align: justify;\">.{context_str}"
        )
        sec_data = _fetch_ai(sec_query)

        if sec_data and 'content' in sec_data:
            content = sec_data['content']
            content = re.sub(r'<table.*?</table>', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<div class="mbtTOC".*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<script>mbtTOC.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<!---.*?--->', '', content, flags=re.DOTALL | re.IGNORECASE)
            full_html += f"\n\n<!-- Section: {section} -->\n" + content
        else:
            print(f"[!] Warning: Failed to generate section '{section}'")
    full_html += "\n\n<!--- TABLE OF CONTENT START 2215587-->\n<script>mbtTOC();</script>\n<!--- TABLE OF CONTENT END 2215587-->"
    wc = _word_count(full_html)
    _log(MSG_COMPLETE, wc=wc, min=BLOG_POST_MIN_WORDS, max=BLOG_POST_MAX_WORDS)
    return {'title': final_title, 'content': full_html, 'labels': final_labels}

def _truncate_to_words(html, max_words):
    if _word_count(html) <= max_words:
        return html
    words = re.sub(r"<[^>]+>", " ", html).split()[:max_words]
    return "<p>" + " ".join(words) + "</p>"

def post_to_blogger(title, content, labels=None):
    if not BLOGGER_BLOG_ID:
        print("[!] BLOGGER_BLOG_ID not set. Skipping post.")
        return None
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"[!] {CREDENTIALS_FILE} not found. Skipping post.")
        return None
    creds = get_credentials()
    service = build('blogger', 'v3', credentials=creds)
    post = {'kind': 'blogger#post', 'blog': {'id': BLOGGER_BLOG_ID}, 'title': title, 'content': content}
    if labels:
        post['labels'] = list(labels)[:20]
    result = service.posts().insert(blogId=BLOGGER_BLOG_ID, body=post).execute()
    print(f"Posted: {result.get('url')}")
    return result

def auto_post(news_items=None):
    topic = (TOPIC and TOPIC.strip()) or None
    if topic and topic not in TOPICS:
        topic = random.choice(TOPICS)
    elif not topic:
        topic = random.choice(TOPICS)
    print(f"[+] Generating blog post about: {topic}")
    data = generate_ai_content(topic, context_news=news_items)
    if isinstance(data, dict):
        title = (data.get('title') or 'Untitled')[:POST_TITLE_MAX_CHARS]
        content = data.get('content') or ''
        labels = data.get('labels') or []
    else:
        lines = (data or '').split('\n')
        title = (lines[0].replace('#', '').strip() if lines else 'Untitled')[:POST_TITLE_MAX_CHARS]
        content = '\n'.join(lines[1:]) if len(lines) > 1 else (data or '')
        labels = []
    wc = _word_count(content)
    if not FORCE_POST and wc < BLOG_POST_MIN_WORDS:
        print(f"[!] Skipping post: {wc} words < min {BLOG_POST_MIN_WORDS} (set FORCE_POST=true to post anyway)")
        return
    if wc > BLOG_POST_MAX_WORDS:
        content = _truncate_to_words(content, BLOG_POST_MAX_WORDS)
        print(f"[+] Truncated to {BLOG_POST_MAX_WORDS} words")
    print(f"[+] Generated title: {title}")
    post_to_blogger(title, content, labels)

if __name__ == '__main__':
    auto_post()
