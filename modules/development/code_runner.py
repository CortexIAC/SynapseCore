from modules.base_module import BaseModule


class CodeRunnerModule(BaseModule):
    name = "Code Runner"
    interface = "development"

    def __init__(self, runtime):
        self.runtime = runtime

    def run(self, code):
        return f"[DEV] Running:\n{code}"