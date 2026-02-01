import os
import json
import requests
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import random
from config import CREDENTIALS_FILE, TOKEN_FILE, BLOGGER_BLOG_ID, WORKER_URL, TOPIC, TOPICS

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


def _fetch_from_worker(query, session_id):
    """Internal helper to fetch JSON from worker with retry/parsing logic"""
    try:
        url = f"{WORKER_URL}?q={requests.utils.quote(query)}&session={session_id}"
        # We use a long timeout for each section as they are now deeply researched
        response = requests.get(url, timeout=1200)
        response.raise_for_status()
        text = response.text.strip()
        
        # Clean markdown if present
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        # Robust JSON cleaning: allow control characters inside string values
        try:
            # strict=False allows control characters like raw newlines inside strings
            return json.loads(text, strict=False)
        except json.JSONDecodeError:
            # Fallback for more serious issues (like missing quotes or unescaped slashes)
            import re
            fixed_text = re.sub(r'(?<!\\)\n', r'\\n', text)
            fixed_text = fixed_text.replace('\r', '\\r').replace('\t', '\\t')
            return json.loads(fixed_text, strict=False)
    except Exception as e:
        print(f"[!] Worker error for query '{query[:50]}...': {e}")
        return None

def generate_ai_content(topic=None):
    """Generate a MASSIVE 10,000+ word blog post using section-by-section generation"""
    session_id = 'mass_post_' + str(hash(topic or 'default'))[:8]
    selected_topic = topic or random.choice(TOPICS)
    
    print(f"[+] Starting MASSIVE generation for: {selected_topic}")
    
    # Step 1: Get Outline
    print(f"[+] PHASE 1: Generating detailed 15-section outline...")
    outline_data = _fetch_from_worker(f"outline: {selected_topic}", session_id)
    if not outline_data or 'sections' not in outline_data:
        print("[!] Failed to get outline. Using fallback single-shot generation.")
        fallback_query = f"generate {selected_topic}"
        return _fetch_from_worker(fallback_query, session_id) or {'title': selected_topic, 'content': '<p>Content generation failed.</p>', 'labels': ['error']}

    sections = outline_data['sections']
    print(f"[+] Outline ready with {len(sections)} sections.")

    # Step 2: Get Content for each section
    full_html = ""
    # The first section is special: it contains the Title, Header Image, and Intro
    print(f"[+] PHASE 2: Generating Header and Introduction...")
    header_data = _fetch_from_worker(f"section: Introduction and Title |topic: {selected_topic}", session_id)
    if header_data:
        full_html += header_data.get('content', '')
        final_labels = header_data.get('labels', [])
        final_title = header_data.get('title', f"The Ultimate Guide to {selected_topic}")
    else:
        final_labels = ["education", selected_topic.lower()]
        final_title = f"The Definitive Guide to {selected_topic}"

    # Generate subsequent sections
    for i, section in enumerate(sections[1:], 2):
        print(f"[+] PHASE 2: Generating section {i}/{len(sections)}: {section}")
        sec_data = _fetch_from_worker(f"section: {section} |topic: {selected_topic}", session_id)
        if sec_data and 'content' in sec_data:
            content = sec_data['content']
            # Remove duplicating elements like TOC or header tables from segments
            import re
            content = re.sub(r'<table.*?</table>', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<div class="mbtTOC".*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<script>mbtTOC.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<!---.*?--->', '', content, flags=re.DOTALL | re.IGNORECASE)
            
            full_html += f"\n\n<!-- Section: {section} -->\n" + content
        else:
            print(f"[!] Warning: Failed to generate section '{section}'")

    # Add Footer TOC script at the very end to ensure all injected H2s are captured
    full_html += "\n\n<!--- TABLE OF CONTENT START 2215587-->\n<script>mbtTOC();</script>\n<!--- TABLE OF CONTENT END 2215587-->"
    
    print(f"[+] MASSIVE Generation Complete! Combined HTML length: {len(full_html)} chars.")
    
    return {
        'title': final_title,
        'content': full_html,
        'labels': final_labels
    }

def post_to_blogger(title, content, labels=None):
    if not BLOGGER_BLOG_ID:
        print("[!] BLOGGER_BLOG_ID not set. Skipping post.")
        print(f"Would post: {title}")
        return None
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"[!] {CREDENTIALS_FILE} not found. Skipping post.")
        print(f"Would post: {title}")
        return None
    creds = get_credentials()
    service = build('blogger', 'v3', credentials=creds)
    post = {
        'kind': 'blogger#post',
        'blog': {'id': BLOGGER_BLOG_ID},
        'title': title,
        'content': content
    }
    if labels:
        post['labels'] = list(labels)[:20]
    request = service.posts().insert(blogId=BLOGGER_BLOG_ID, body=post)
    result = request.execute()
    print(f"Posted: {result.get('url')}")
    return result

def auto_post():
    """Generate and post a blog article about an allowed topic"""
    # Get topic from environment or choose random from allowed list
    topic = (TOPIC and TOPIC.strip()) or None
    
    # Validate topic is in allowed list
    if topic and topic not in TOPICS:
        print(f"[!] Warning: Selected topic '{topic}' is not in allowed topics list.")
        print(f"[!] Allowed topics: {', '.join(TOPICS)}")
        print(f"[!] Defaulting to random allowed topic...")
        topic = random.choice(TOPICS)
    elif not topic:
        topic = random.choice(TOPICS)
    
    print(f"[+] Generating blog post about: {topic}")
    print(f"[+] Allowed topics: {', '.join(TOPICS)}")
    
    # Generate content
    data = generate_ai_content(topic)
    
    # Parse the generated data
    if isinstance(data, dict):
        title = (data.get('title') or 'Untitled')[:100]
        content = data.get('content') or ''
        labels = data.get('labels') or []
    else:
        lines = (data or '').split('\n')
        title = lines[0].replace('#', '').strip()[:100]
        content = '\n'.join(lines[1:]) if len(lines) > 1 else (data or '')
        labels = []
    
    print(f"[+] Generated title: {title}")
    print(f"[+] Generated {len(labels)} labels: {', '.join(labels) if labels else 'None'}")
    
    # Post to blogger
    post_to_blogger(title, content, labels)


if __name__ == '__main__':
    auto_post()

