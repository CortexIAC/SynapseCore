class BaseModule:
    name = "Base"
    interface = "default"

    def __init__(self, runtime):
        self.runtime = runtime

    def run(self, *args, **kwargs):
        raise NotImplementedError("Module must implement run()")