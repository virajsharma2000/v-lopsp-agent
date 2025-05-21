import os
import time
import json
import requests
from datetime import datetime, timedelta

OLLAMA_MODEL = "llama3"
OLLAMA_URL = "http://localhost:11434/api/generate"
PROMPT_HISTORY_FILE = "joke_history.json"

# === Save & Load State ===
def load_history():
    if os.path.exists(PROMPT_HISTORY_FILE):
        with open(PROMPT_HISTORY_FILE, "r") as f:
            return json.load(f)
    return {"last_prompt": "Tell me a joke!", "next_check": None, "condition": None}

def save_history(state):
    with open(PROMPT_HISTORY_FILE, "w") as f:
        json.dump(state, f)

# === Call Ollama ===
def call_ollama(prompt):
    response = requests.post(OLLAMA_URL, json={
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]

# === Parse LLM Response to Get Next Trigger ===
def parse_llm_response(response):
    # We'll look for instructions like: "Check again in 30 seconds or when file 'tell_joke.txt' exists."
    delay = 60  # default
    condition_file = "tell_joke.txt"

    if "15" in response or "fifteen" in response:
        delay = 15
    elif "30" in response:
        delay = 30
    elif "5" in response:
        delay = 5

    if ".txt" in response:
        condition_file = response.split("file")[1].split()[0].strip("'\".")

    return delay, condition_file

# === Main Loop ===
def main():
    state = load_history()
    print("[LOPSP Agent] Starting...")

    while True:
        now = datetime.now()

        # Check if condition met
        condition_met = state["condition"] and os.path.exists(state["condition"])
        time_met = not state["next_check"] or now >= datetime.fromisoformat(state["next_check"])

        if condition_met or time_met:
            prompt = state["last_prompt"]
            print(f"\n---\n[Prompting LLM]: {prompt}")
            response = call_ollama(prompt)
            print(f"[LLM Response]: {response.strip()}\n")

            delay, condition_file = parse_llm_response(response)
            next_time = datetime.now() + timedelta(seconds=delay)

            state = {
                "last_prompt": "Can you tell me another joke and when to ask again?",
                "next_check": next_time.isoformat(),
                "condition": condition_file
            }

            save_history(state)

            # Clean up condition file if used
            if os.path.exists(condition_file):
                os.remove(condition_file)

        time.sleep(1)

if __name__ == "__main__":
    main()
