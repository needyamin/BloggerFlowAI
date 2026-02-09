import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

key = os.getenv('GEMINI_API_KEY', '').strip()
if not key:
    print("No API key")
    exit()

genai.configure(api_key=key)
print("Available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
