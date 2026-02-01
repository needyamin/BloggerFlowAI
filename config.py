import os
from dotenv import load_dotenv

load_dotenv()

BLOGGER_BLOG_ID = os.getenv('BLOGGER_BLOG_ID','3422137415075355570')
WORKER_URL = os.getenv('WORKER_URL', 'https://gpt-oss-auto-post.md-yamin-hossain.workers.dev').rstrip('/')
TOPIC = os.getenv('TOPIC')
TOPICS = [
    'Education', 'Scholarship Abroad', 'Latest Technology News',
    'Scholarship in USA/Japan/UK', 'Global Breaking News', 'Viral News', 'Secret Societies'
]
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

