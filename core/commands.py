from core.memory import Memory


class CommandRouter:
    def __init__(self, state, ui):
        self.state = state
        self.ui = ui
        self.memory = Memory()

        self.commands = {
            "help": self.help,
            "remember": self.remember,
            "what is": self.recall,
            "what's": self.recall,
            "open": self.open_cmd,
            "switch to": self.switch_tab,
            "close": self.close_tab,
            "shutdown": self.shutdown,
            "shut down": self.shutdown,
            "exit": self.shutdown,
        }

    # ========================
    # MAIN
    # ========================

    def handle(self, text):
        text = text.lower().strip()

        if hasattr(self.ui, "debug"):
            self.ui.debug(f"[COMMAND] {text}")

        for cmd in self.commands:
            if cmd in text:
                return self.commands[cmd](text)

        return "I don’t understand"

    # ========================
    # MEMORY
    # ========================

    def remember(self, text):
        raw = text.lower().strip()

        # natural phrases
        if "my name is" in raw:
            key = "my name"
            value = raw.split("my name is", 1)[1].strip()

        elif "call me" in raw:
            key = "my name"
            value = raw.split("call me", 1)[1].strip()

        elif " is " in raw:
            raw = raw.replace("remember", "", 1).strip()
            key, value = raw.split(" is ", 1)

        else:
            return "Try: remember my name is Dom"

        if not value:
            return "I didn’t catch the value"

        corrections = {
            "don": "Dom",
            "dumb": "Dom",
            "tom": "Dom"
        }

        value = corrections.get(value.lower(), value.capitalize())

        self.memory.set(key.strip(), value)

        return f"Remembered {key.strip()} = {value}"

    def recall(self, text):
        key = text.replace("what is", "").replace("what's", "").strip()
        value = self.memory.get(key)

        if value:
            return f"{key} is {value}"

        return "I don’t know"

    # ========================
    # BROWSER
    # ========================

    def open_cmd(self, text):
        target = text.replace("open", "").strip()

        if not target:
            return "Open what?"

        if " " in target:
            url = f"https://www.google.com/search?q={target.replace(' ', '+')}"
        else:
            url = f"https://{target}.com"

        if hasattr(self.ui, "debug"):
            self.ui.debug(f"[BROWSER] Opening {url}")

        self.ui.new_tab(url)
        self.ui.switch_tab(len(self.ui.tabs_list) - 1)
        self.ui.go_to_web()

        return f"Opening {url}"

    def switch_tab(self, text):
        target = text.replace("switch to", "").strip()

        if self.ui.switch_main_tab(target):
            return f"Switched to {target}"

        for i, tab in enumerate(self.ui.tabs_list):
            if target in tab.get("title", "").lower():
                self.ui.switch_tab(i)
                self.ui.go_to_web()
                return f"Switched to {target}"

        return "Tab not found"

    def close_tab(self, text):
        target = text.replace("close", "").replace("tab", "").strip().lower()

        if not target:
            i = self.ui.tabs_list.index(self.ui.current_tab)
            self.ui.close_tab(i)
            return "Closed tab"

        for i, tab in enumerate(self.ui.tabs_list):
            if target in tab.get("title", "").lower():
                self.ui.close_tab(i)
                return f"Closed {target}"

        return "Tab not found"

    # ========================
    # SYSTEM
    # ========================

    def shutdown(self, text):
        try:
            for tab in getattr(self.ui, "tabs_list", []):
                try:
                    tab["browser"].close()
                except:
                    pass

            self.ui.root.after(0, self.ui.root.destroy)

            return "Shutting down..."

        except Exception as e:
            return str(e)

    def help(self, text):
        return "I can open sites, remember things, and control tabs."