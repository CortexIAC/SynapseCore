from modules.base_module import BaseModule


class QuickBMSModule(BaseModule):
    name = "QuickBMS"
    interface = "modding"

    def run(self, file):
        return f"[MODDING] Extracting: {file}"