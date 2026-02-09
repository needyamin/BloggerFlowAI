"""
Test script for Google Gemini API integration
Run this to verify your Gemini API is working correctly
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
src_path = str(Path(__file__).resolve().parent.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from models.remote_agent import fetch_gemini

load_dotenv()


def test_gemini():
    """Test Google Gemini API integration"""
    
    print("=" * 60)
    print("=" * 60)
    print("Testing Google Gemini API Integration")
    print("=" * 60)
    
    # Check if API key is set
    api_key = os.getenv('GEMINI_API_KEY', '').strip()
    
    if not api_key or api_key == 'YOUR_GEMINI_API_KEY_HERE':
        print("[!] ERROR: GEMINI_API_KEY not set!")
        print("\nTo fix this:")
        print("1. Get your API key from: https://aistudio.google.com/app/apikey")
        print("2. Open .env file")
        print("3. Replace 'YOUR_GEMINI_API_KEY_HERE' with your actual key")
        print("\nExample:")
        print("GEMINI_API_KEY=AIzaSyC...")
        return
    
    print(f"[+] API Key found: {api_key[:10]}...{api_key[-4:]}")
    print("\n" + "-" * 60)
    
    # Test 1: Outline Generation
    print("\n[PHASE 1] Test 1: Generating Blog Post Outline...")
    print("Topic: Latest Technology News")
    
    try:
        result = fetch_gemini("outline: Latest Technology News")
        
        if result and 'sections' in result:
            print("[+] Outline generation SUCCESS!")
            print(f"\nGenerated {len(result.get('sections', []))} sections:")
            for i, section in enumerate(result.get('sections', [])[:5], 1):
                print(f"  {i}. {section}")
            if len(result.get('sections', [])) > 5:
                print(f"  ... and {len(result.get('sections', [])) - 5} more sections")
        else:
            print("[!] Outline generation FAILED!")
            print(f"Response: {result}")
            
    except Exception as e:
        print(f"[!] ERROR: {e}")
    
    print("\n" + "-" * 60)
    
    # Test 2: Section Content Generation
    print("\n[PHASE 2] Test 2: Generating Section Content...")
    print("Section: Introduction to AI")
    
    try:
        result = fetch_gemini("section: Introduction to AI|topic:Latest Technology News")
        
        if result and 'content' in result:
            print("[+] Section generation SUCCESS!")
            content = result.get('content', '')
            word_count = len(content.split())
            print(f"\nGenerated content:")
            print(f"  - Word count: {word_count}")
            print(f"  - Has HTML: {'Yes' if '<p' in content else 'No'}")
            print(f"  - Title: {result.get('title', 'N/A')}")
            print(f"  - Labels: {result.get('labels', [])}")
            
            # Show first 200 chars of content
            preview = content[:200].replace('\n', ' ')
            print(f"\n  Preview: {preview}...")
        else:
            print("[!] Section generation FAILED!")
            print(f"Response: {result}")
            
    except Exception as e:
        print(f"[!] ERROR: {e}")
    
    print("\n" + "-" * 60)
    
    # Test 3: Full Post Generation
    print("\n[PHASE 3] Test 3: Generating Full Blog Post...")
    print("Topic: AI and Machine Learning")
    
    try:
        result = fetch_gemini("generate AI and Machine Learning")
        
        if result:
            print("[+] Full post generation SUCCESS!")
            print(f"\nGenerated post:")
            print(f"  - Title: {result.get('title', 'N/A')}")
            
            content = result.get('content', '')
            word_count = len(content.split())
            print(f"  - Word count: {word_count}")
            print(f"  - Labels: {result.get('labels', [])}")
            print(f"  - Has HTML: {'Yes' if '<p' in content else 'No'}")
            
        else:
            print("[!] Full post generation FAILED!")
            print(f"Response: {result}")
            
    except Exception as e:
        print(f"[!] ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("[+] Gemini API Testing Complete!")
    print("=" * 60)
    print("\nIf all tests passed, your Gemini API is working correctly!")
    print("   You can now use it as a fallback for blog post generation.\n")

if __name__ == '__main__':
    test_gemini()
