#!/usr/bin/env python3
"""
Verification script to check if your environment is set up correctly.
Run this before starting the app to verify everything is configured.
"""

import os
from pathlib import Path

def verify_setup():
    print("=" * 60)
    print("Smart Quizzer - Setup Verification")
    print("=" * 60)
    print()
    
    # Show current working directory
    print(f"Current directory: {os.getcwd()}")
    print()
    
    # Check if .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ ERROR: .env file not found!")
        print()
        print("To fix this:")
        print("1. Copy .env.example to .env:")
        print("   cp .env.example .env")
        print()
        print("2. Edit .env and add your Groq API key:")
        print("   GROQ_API_KEY=your_actual_api_key_here")
        print()
        return False
    else:
        print("✓ .env file exists")
        print(f"  Location: {env_file.absolute()}")
        print(f"  Size: {env_file.stat().st_size} bytes")
        print()
        print("Contents of .env file (API keys masked):")
        print("-" * 60)
        with open('.env', 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.rstrip()
                if 'GROQ_API_KEY' in line and '=' in line:
                    parts = line.split('=', 1)
                    if len(parts) == 2 and parts[1].strip():
                        key_preview = parts[1].strip()
                        if len(key_preview) > 8:
                            masked = f"{key_preview[:4]}...{key_preview[-4:]}"
                        else:
                            masked = "***"
                        print(f"  Line {line_num}: {parts[0]}={masked}")
                    else:
                        print(f"  Line {line_num}: {line} (⚠️ NO VALUE AFTER =)")
                elif line.strip() and not line.strip().startswith('#'):
                    print(f"  Line {line_num}: {line}")
                elif line.strip().startswith('#'):
                    print(f"  Line {line_num}: {line}")
        print("-" * 60)
        print()
    
    # Try to load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv(override=True, verbose=True)
        print("✓ python-dotenv is installed and loaded")
    except ImportError:
        print("❌ ERROR: python-dotenv not installed!")
        print("   Run: pip install python-dotenv")
        return False
    
    # Check if API key is set
    api_key = os.getenv('GROQ_API_KEY')
    
    print()
    print("Environment variable check:")
    print(f"  GROQ_API_KEY found: {api_key is not None}")
    if api_key:
        print(f"  Length: {len(api_key)} characters")
        print(f"  Starts with: {api_key[:4] if len(api_key) >= 4 else api_key}")
        print(f"  Ends with: {api_key[-4:] if len(api_key) >= 4 else api_key}")
        print(f"  Contains whitespace: {any(c.isspace() for c in api_key)}")
    print()
    
    if not api_key:
        print("❌ ERROR: GROQ_API_KEY not found in environment!")
        print()
        print("To fix this:")
        print("1. Make sure your .env file has a line like:")
        print("   GROQ_API_KEY=gsk_your_actual_key_here")
        print()
        print("2. Make sure there are NO SPACES around the = sign")
        print("3. Make sure the key is on a single line")
        print("4. Get your key from: https://console.groq.com/keys")
        print()
        return False
    elif api_key == 'your_groq_api_key_here':
        print("❌ ERROR: GROQ_API_KEY is still set to placeholder value!")
        print()
        print("To fix this:")
        print("1. Get your API key from: https://console.groq.com/keys")
        print("2. Open .env file and replace the placeholder with your real key")
        print()
        return False
    elif len(api_key) < 20:
        print("⚠️  WARNING: GROQ_API_KEY seems too short!")
        print(f"   Current length: {len(api_key)} characters")
        print("   Expected: 50+ characters")
        print()
        print("   Make sure you copied the entire API key from Groq console")
        return False
    else:
        # Show first and last 4 characters of API key for verification
        masked_key = f"{api_key[:4]}...{api_key[-4:]}"
        print(f"✓ GROQ_API_KEY is set: {masked_key}")
    
    # Test Groq API connection
    print()
    print("Testing Groq API connection...")
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        
        # Try a simple API call
        response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # ✅ supported
        messages=[{"role": "user", "content": "Hello Groq"}],
        max_tokens=20
        )

        
        print("✓ Groq API connection successful!")
        print()
        print("=" * 60)
        print("✓ All checks passed! You're ready to run the app.")
        print("=" * 60)
        print()
        print("Run the app with: python app.py")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Failed to connect to Groq API!")
        print(f"   Error: {str(e)}")
        print()
        print("Possible issues:")
        print("1. Invalid API key - verify your key at https://console.groq.com/keys")
        print("2. Network connection issues")
        print("3. Groq API service is down")
        print()
        print("Double-check your API key:")
        print(f"  Current key: {api_key[:4]}...{api_key[-4:]}")
        return False

if __name__ == '__main__':
    success = verify_setup()
    exit(0 if success else 1)
