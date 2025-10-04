# Project Arts Detection Script
import time
import requests
import hashlib
import json

# URLs
ART_URL = "https://raw.githubusercontent.com/ProjectArtsAnimations/Project-Arts/refs/heads/main/Main.txt"
TRIGGER_URL = "https://raw.githubusercontent.com/ProjectArtsAnimations/Project-Arts/refs/heads/main/TestPaste.json"

# Time interval for checking (in seconds)
CHECK_INTERVAL = 10

def fetch_text(url):
    """Fetch plain text from a URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"[ERROR] Could not fetch {url}: {e}")
        return None

def fetch_json(url):
    """Fetch JSON data from a URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[ERROR] Could not fetch {url}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON from {url}: {e}")
        return None

def hash_text(text):
    """Return MD5 hash of text for change detection."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def print_ascii_art(art_content):
    """Print ASCII art to console."""
    print("\n" + art_content + "\n")

def monitor_art_and_trigger():
    """Monitor both Main.txt and TestPaste.json for changes."""
    last_art_hash = None
    last_trigger_hash = None

    while True:
        # Fetch ASCII art
        art_content = fetch_text(ART_URL)
        if art_content is None:
            print("[WARNING] Failed to fetch Main.txt. Retrying...")
        else:
            current_art_hash = hash_text(art_content)
            if current_art_hash != last_art_hash:
                print("[UPDATE] Change detected in Main.txt!")
                print_ascii_art(art_content)
                last_art_hash = current_art_hash

        # Fetch JSON trigger
        trigger_data = fetch_json(TRIGGER_URL)
        if trigger_data is None:
            print("[WARNING] Failed to fetch TestPaste.json. Retrying...")
        else:
            trigger_str = json.dumps(trigger_data, sort_keys=True)
            current_trigger_hash = hash_text(trigger_str)
            if current_trigger_hash != last_trigger_hash:
                print("[UPDATE] Change detected in TestPaste.json!")
                # Optional: Could also print trigger content or just refresh art
                if art_content:
                    print_ascii_art(art_content)
                last_trigger_hash = current_trigger_hash

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    print("[INFO] Starting Project Art Detection...")
    monitor_art_and_trigger()
