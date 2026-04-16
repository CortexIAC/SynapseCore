# engine.py


import os
import importlib.util

class AIEngine:
    def __init__(self):
        self.modules = {}

    # ✅ keep this (optional but useful)
    def register_module(self, name, module):
        self.modules[name] = module

    # ✅ REQUIRED (this is what runtime is calling)
    def load_modules(self, base_path="modules"):
        self.modules.clear()

        for root, _, files in os.walk(base_path):
            for file in files:
                if not file.endswith(".py"):
                    continue

                filepath = os.path.join(root, file)
                module_name = os.path.splitext(file)[0]

                try:
                    spec = importlib.util.spec_from_file_location(module_name, filepath)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)

                    for attr in dir(mod):
                        obj = getattr(mod, attr)

                        if isinstance(obj, type) and hasattr(obj, "run"):
                            instance = obj()

                            name = module_name.replace("_module", "")
                            self.modules[name] = instance

                            print(f"[Engine] Loaded module: {name}")

                except Exception as e:
                    print(f"[Engine] Failed to load {file}: {e}")

    def run(self, command):
        command = command.strip().lower()

        if command in self.modules:
            module = self.modules[command]

            if hasattr(module, "run"):
                return module.run()

        return None