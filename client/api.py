from typing import List, Dict, Any
import requests

BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 3.0  # Clear constant for network boundaries

def submit_score(player_name: str, score: int) -> bool:
    """Sends an HTTP POST request to submit a player's score to the backend."""
    url = f"{BASE_URL}/score"
    payload = {"player_name": player_name, "score": score}
    try:
        response = requests.post(url, json=payload, timeout=TIMEOUT)
        if response.status_code == 200:
            return bool(response.json().get("success", False))
        return False
    except requests.RequestException:
        print("Backend unavailable. Using offline mode.")
        return False

def get_leaderboard() -> List[Dict[str, Any]]:
    """Calls GET /leaderboard to fetch sorted scores from the database."""
    url = f"{BASE_URL}/leaderboard"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                return data
        return []
    except requests.RequestException:
        print("Backend unavailable. Using offline mode.")
        return []