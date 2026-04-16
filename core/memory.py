import json
import os

MEMORY_FILE = "data/memory.json"


class Memory:
    def __init__(self):
        os.makedirs("data", exist_ok=True)

        if not os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "w") as f:
                json.dump({}, f)

        self.data = self.load()

    def load(self):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except:
            return {}

    def save(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def get(self, key):
        return self.data.get(key)