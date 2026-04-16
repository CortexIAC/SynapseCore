import json
import os
from datetime import datetime

MEMORY_FILE = "long_term_memory.json"


class Memory:
    def __init__(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    self.data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.data = []
        else:
            self.data = []

    def add(self, user, assistant):
        self.data.append({
            "user": user,
            "assistant": assistant,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # keep last 100 entries
        self.data = self.data[-100:]

        with open(MEMORY_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def get_context(self):
        return "\n".join(
            f"User: {x['user']}\nAssistant: {x['assistant']}"
            for x in self.data[-5:]
        )