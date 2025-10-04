import time
import requests
import json

# URLs
ART_URL = "https://raw.githubusercontent.com/ProjectArtsAnimations/Project-Arts/refs/heads/main/Main.txt"
TRIGGER_URL = "https://raw.githubusercontent.com/ProjectArtsAnimations/Project-Arts/refs/heads/main/TestPaste.json"

def fetch_text(url):
    """Fetch plain text from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def fetch_json(url):
    """Fetch JSON data from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {url}: {e}")
        return None

def print_ascii_art():
    """Fetch and print ASCII art from Main.txt."""
    art = fetch_text(ART_URL)
    if art:
        print("\n" + art + "\n")

def monitor_changes():
    """Monitor the JSON trigger for changes."""
    last_trigger = None
    while True:
        json_data = fetch_json(TRIGGER_URL)
        if json_data is None:
            print("Failed to fetch JSON. Retrying in 5 seconds...")
            time.sleep(5)
            continue

        trigger_value = json_data.get("ascii_trigger")
        if trigger_value != last_trigger:
            print("Change detected in JSON trigger! Updating ASCII art...")
            print_ascii_art()
            last_trigger = trigger_value
        else:
            print("No change detected. Waiting...")

        time.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    monitor_changes()
