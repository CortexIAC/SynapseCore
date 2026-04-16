from ai.ollama_backend import chat_ollama
from ai.memory import Memory

memory = Memory()


# ========================
# MODULE MATCHING
# ========================
def keyword_fallback(text, state):
    text_lower = text.lower()

    for name in state.engine.modules:
        if name in text_lower:
            print(f"[Fallback] Matched: {name}")
            return name

    return None


def choose_module_with_ai(text, state):
    # placeholder for future AI-based routing
    return None


# ========================
# MAIN ROUTER
# ========================
def chat(text, state):
    app = getattr(state, "app", None)

    def debug(msg):
        if app and hasattr(app, "debug"):
            app.debug(msg)
        else:
            print(msg)

    text_lower = text.lower().strip()

    # ========================
    # 🔥 UI COMMANDS FIRST
    # ========================
    if "switch to" in text_lower:
        tab = text_lower.replace("switch to", "").strip()

        if app and hasattr(app, "switch_main_tab"):
            app.switch_main_tab(tab)
            return f"Switched to {tab}"

        return "[UI not ready]"

    if text_lower.startswith("open "):
        target = text_lower.replace("open ", "").strip()
        url = f"https://{target}.com"

        if app and hasattr(app, "open_browser"):
            app.open_browser(url)

        return f"Opening {url}"

    # ========================
    # 🧩 MODULE SYSTEM
    # ========================
    chosen = None

    # ✅ ONLY run module system if engine exists
    if hasattr(state, "engine"):
        try:
            chosen = choose_module_with_ai(text, state)
            debug(f"[AI Router] → {chosen}")
        except Exception as e:
            debug(f"[AI Error] {e}")

        if not chosen:
            chosen = keyword_fallback(text, state)
            debug(f"[Fallback] → {chosen}")

        if chosen and chosen in state.engine.modules:
            debug(f"[Engine] Running module: {chosen}")
            result = state.engine.run(chosen)
            return str(result)

    # ========================
    # 🤖 FALLBACK TO AI
    # ========================
    try:
        return chat_ollama(text)
    except Exception as e:
        return f"[AI ERROR] {e}"