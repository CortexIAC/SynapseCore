class ModuleManager:
    def __init__(self, runtime):
        self.runtime = runtime
        self.modules = {}

    def register(self, module):
        self.modules[module.name] = module

    def get(self, name):
        return self.modules.get(name)

    def all(self):
        return list(self.modules.values())

    def get_modules_for_interface(self, interface):
        return [
            m for m in self.modules.values()
            if getattr(m, "interface", None) == interface
        ]