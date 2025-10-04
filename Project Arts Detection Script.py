import time
import requests
import hashlib
import json
from datetime import datetime

ART_URL = "https://raw.githubusercontent.com/ProjectArtsAnimations/Project-Arts/main/Main.txt"
TRIGGER_URL = "https://raw.githubusercontent.com/ProjectArtsAnimations/Project-Arts/main/TestPaste.json"
LOG_FILE = "Project Arts Logs.txt"
CHECK_INTERVAL = 10

def fetch_text(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"[ERROR] Could not fetch {url}: {e}")
        return None

def fetch_json(url):
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
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def print_ascii_art(art_content):
    print("\n" + art_content + "\n")

def log_ascii_art(art_content):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"--- {timestamp} ---\n")
        f.write(art_content + "\n\n")

def monitor_and_log():
    print("[INFO] Starting Project Arts Live Logging...")
    last_art_hash = None
    last_trigger_hash = None

    while True:
        # Fetch ASCII art
        art_content = fetch_text(ART_URL)
        if art_content:
            current_art_hash = hash_text(art_content)
            if last_art_hash is None or current_art_hash != last_art_hash:
                print("[UPDATE] Main.txt detected!")
                print_ascii_art(art_content)
                log_ascii_art(art_content)
                last_art_hash = current_art_hash
        else:
            print("[DEBUG] Failed to fetch Main.txt.")

        # Fetch JSON trigger
        trigger_data = fetch_json(TRIGGER_URL)
        if trigger_data:
            trigger_str = json.dumps(trigger_data, sort_keys=True)
            current_trigger_hash = hash_text(trigger_str)
            if last_trigger_hash is None or current_trigger_hash != last_trigger_hash:
                print("[UPDATE] TestPaste.json changed!")
                if art_content:
                    print_ascii_art(art_content)
                    log_ascii_art(art_content)
                last_trigger_hash = current_trigger_hash
        else:
            print("[DEBUG] Failed to fetch TestPaste.json.")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_and_log()
