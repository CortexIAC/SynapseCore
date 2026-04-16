import json
import os

# ===== FILE PATH =====
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.json")


# =========================
# LOAD / SAVE
# =========================
def _load():
    if not os.path.exists(USERS_FILE):
        return {}

    try:
        with open(USERS_FILE, "r") as f:
            data = json.load(f)

            # 🔥 auto-upgrade old format
            if "username" in data:
                return {
                    data["username"]: {
                        "password": data.get("password", ""),
                        "role": data.get("role", "user"),
                        "ollama_model": data.get("ollama_model", "")
                    }
                }

            return data

    except:
        return {}


def _save(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=2)


# =========================
# AUTH
# =========================
def verify_login(username, password):
    data = _load()

    if username not in data:
        return False

    return data[username].get("password") == password


def create_profile(username, password):
    data = _load()

    if username in data:
        return False  # already exists

    data[username] = {
        "password": password,
        "role": "user",
        "ollama_model": ""
    }

    _save(data)
    return True


def get_profile_names():
    data = _load()
    return list(data.keys())


# =========================
# ROLES
# =========================
def get_role(username):
    data = _load()
    return data.get(username, {}).get("role", "user")


def set_role(username, role):
    data = _load()

    if username not in data:
        return False

    data[username]["role"] = role
    _save(data)
    return True


# =========================
# MODEL
# =========================
def set_user_model(username, model):
    data = _load()

    if username not in data:
        return False

    data[username]["ollama_model"] = model
    _save(data)
    return True


def get_user_model(username):
    data = _load()
    return data.get(username, {}).get("ollama_model", "")