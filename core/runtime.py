import tkinter as tk
from tkinter import ttk
from core.state import SystemState
from core.voice_controller import VoiceController

from modules.module_manager import ModuleManager

from modules.development.code_runner import CodeRunnerModule
from modules.modding.quickbms_module import QuickBMSModule
from modules.security.nmap_module import NmapModule

class Runtime:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI OS")
        self.root.configure(bg="#020402")
        self.root.state("zoomed")
        self.voice_callback = None

        self.module_manager = ModuleManager(self)

        self.module_manager.register(CodeRunnerModule(self))
        self.module_manager.register(QuickBMSModule(self))
        self.module_manager.register(NmapModule(self))

        self.voice = VoiceController(self)

        # ✅ ADD THIS (missing before)
        self.debug_callback = None

        self.state = SystemState()
        self.current_view = None

        # ✅ STYLE MUST BE AFTER Tk()
        style = ttk.Style(self.root)
        style.theme_use('default')  # or 'clam'

        style.configure("TNotebook", background="#020402", borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background="#003322",
            foreground="#00ff88",
            padding=[10, 5]
        )

        style.map(
            "TNotebook.Tab",
            background=[("selected", "#00ff88")],
            foreground=[("selected", "#002211")]
        )

        self.state = SystemState()
        self.current_view = None

    def debug(self, msg):
        if self.debug_callback:
            self.debug_callback(msg)
        else:
            print(msg)

    def error(self, msg):
        self.debug(f"[ERROR] {msg}")

    def voice_log(self, msg):
        if hasattr(self, "debug_callback") and self.debug_callback:
            self.debug_callback(msg)
        else:
            print(msg)

    # 🔥 CORE VIEW SWITCHER
    def load_view(self, view_class):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.current_view = view_class(self.root, self)

    # ROUTES
    def start(self):
        from ui.startup import StartupScreen
        self.load_view(StartupScreen)

    def load_menu(self):
        from ui.main_menu import MainMenu
        self.load_view(MainMenu)

    def open_framework(self):
        from ui.main_window import MainWindow
        self.load_view(MainWindow)

        print("VOICE STARTING NOW")
        self.voice.start()

    def run(self):
        self.start()
        self.root.mainloop()

    def shutdown(self):
        self.root.quit()

    def code_explain(self, text):
        # later this can call a model / local engine
        return f"[CODE ASSISTANT]\nExplain:\n{text}\n\n(analysis placeholder)"