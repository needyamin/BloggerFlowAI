"""
AI Provider Switcher - Easy way to test different AI providers
Usage: python scripts/switch_ai.py [openai|gemini|all]
"""
import sys
import os
from pathlib import Path

def update_env(provider='all'):
    """Update .env to enable/disable specific AI providers"""
    
    root_dir = Path(__file__).resolve().parent.parent
    env_file = root_dir / '.env'
    
    # Add src to path so we can import config status if needed
    src_path = str(root_dir / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    if not env_file.exists():
        print("[!] .env file not found!")
        return
    
    # Read current .env
    with open(env_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Provider configurations
    configs = {
        'openai': {
            'OPENAI_API_KEY': 'sk-...',  # Keep uncommented
            'GEMINI_API_KEY': None   # Comment out
        },
        'gemini': {
            'OPENAI_API_KEY': None,  # Comment out
            'GEMINI_API_KEY': 'YOUR_GEMINI_API_KEY_HERE'  # Keep uncommented
        },
        'all': {
            'OPENAI_API_KEY': 'sk-...',
            'GEMINI_API_KEY': 'YOUR_GEMINI_API_KEY_HERE'
        }
    }
    
    if provider not in configs:
        print(f"[!] Unknown provider: {provider}")
        print("Available: openai, gemini, all")
        return
    
    print(f"\n[SWITCH] Switching to: {provider.upper()} provider(s)\n")
    
    # Update lines
    new_lines = []
    for line in lines:
        original_line = line
        
        # Handle OPENAI_API_KEY
        if line.strip().startswith('OPENAI_API_KEY=') or line.strip().startswith('# OPENAI_API_KEY='):
            if configs[provider]['OPENAI_API_KEY']:
                # Try to preserve existing key
                if '=' in line and not line.strip().startswith('#'):
                    existing_key = line.split('=', 1)[1].strip()
                    if existing_key and existing_key != 'sk-...':
                        new_lines.append(line)  # Keep existing key
                        print(f"  [+] Enabled: OpenAI API (existing key preserved)")
                    else:
                        new_lines.append(f"OPENAI_API_KEY=sk-...\n")
                        print(f"  [?] Enabled: OpenAI API (needs real API key)")
                else:
                    new_lines.append(f"OPENAI_API_KEY=sk-...\n")
                    print(f"  [?] Enabled: OpenAI API (needs real API key)")
            else:
                new_lines.append(f"# OPENAI_API_KEY=sk-...\n")
                print(f"  [-] Disabled: OpenAI API")
        
        # Handle GEMINI_API_KEY
        elif line.strip().startswith('GEMINI_API_KEY=') or line.strip().startswith('# GEMINI_API_KEY='):
            if configs[provider]['GEMINI_API_KEY']:
                # Try to preserve existing key
                if '=' in line and not line.strip().startswith('#'):
                    existing_key = line.split('=', 1)[1].strip()
                    if existing_key and existing_key != 'YOUR_GEMINI_API_KEY_HERE':
                        new_lines.append(line)  # Keep existing key
                        print(f"  [+] Enabled: Google Gemini API (existing key preserved)")
                    else:
                        new_lines.append(f"GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE\n")
                        print(f"  [?] Enabled: Google Gemini API (needs real API key)")
                else:
                    new_lines.append(f"GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE\n")
                    print(f"  [?] Enabled: Google Gemini API (needs real API key)")
            else:
                new_lines.append(f"# GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE\n")
                print(f"  [-] Disabled: Google Gemini API")
        
        else:
            new_lines.append(original_line)
    
    # Write back
    with open(env_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n[+] Configuration updated in .env")
    print(f"\n[!] Test it now with: python main.py\n")

def show_current():
    """Show currently enabled providers"""
    from dotenv import load_dotenv
    load_dotenv()
    
    print("\n" + "="*60)
    print("CURRENT AI PROVIDER STATUS")
    print("="*60 + "\n")
    
    openai = os.getenv('OPENAI_API_KEY', '').strip()
    gemini = os.getenv('GEMINI_API_KEY', '').strip()
    
    if openai and openai != 'sk-...':
        print("[+] OpenAI API: ENABLED")
        print(f"   Key: {openai[:10]}...{openai[-4:]}")
    elif openai == 'sk-...':
        print("[?] OpenAI API: PLACEHOLDER (needs real key)")
    else:
        print("[-] OpenAI API: DISABLED")
    
    print()
    
    if gemini and gemini != 'YOUR_GEMINI_API_KEY_HERE':
        print("[+] Google Gemini API: ENABLED")
        print(f"   Key: {gemini[:10]}...{gemini[-4:]}")
    elif gemini == 'YOUR_GEMINI_API_KEY_HERE':
        print("[?] Google Gemini API: PLACEHOLDER (needs real key)")
    else:
        print("[-] Google Gemini API: DISABLED")
    
    print("\n" + "="*60 + "\n")

def show_help():
    """Show usage help"""
    print("""
+------------------------------------------------------------+
|         AI Provider Switcher - Quick Configuration         |
+------------------------------------------------------------+

USAGE:
  python scripts/switch_ai.py [provider]

PROVIDERS:
  openai    - Use only OpenAI API - PAID
  gemini    - Use only Google Gemini API - FREE
  all       - Enable all providers (failover chain) - RECOMMENDED
  status    - Show current configuration

EXAMPLES:
  # Use only Gemini (free, reliable)
  python scripts/switch_ai.py gemini

  # Enable all with failover (most reliable)
  python scripts/switch_ai.py all

  # Check current status
  python scripts/switch_ai.py status

NOTES:
  - Gemini API is free with generous limits
  - OpenAI API costs money but is very reliable
  - "all" mode provides best reliability with failover

GET API KEYS:
  OpenAI:  https://platform.openai.com/api-keys
  Gemini:  https://aistudio.google.com/app/apikey
""")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        show_help()
        show_current()
    elif sys.argv[1] == 'status':
        show_current()
    elif sys.argv[1] in ['help', '-h', '--help']:
        show_help()
    elif sys.argv[1] in ['openai', 'gemini', 'all']:
        update_env(sys.argv[1])
        show_current()
    else:
        print(f"[!] Unknown command: {sys.argv[1]}")
        show_help()
