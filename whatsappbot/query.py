import os
from embedchain import App
from django.conf import settings
from embedchain.loaders.directory_loader import DirectoryLoader


class Gen:
    os.environ["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY")
    app = App.from_config(settings.CONFIG_FILE)
    lconfig = {"recursive": True, "extensions": [".doc", ".docx", ".pdf", ".txt"]}
    loader = DirectoryLoader(config=lconfig)

    def __init__(self):
        self.input_knowledge()

    def input_knowledge(self):
        self.app.add(f"{settings.BASE_DIR}/media/kb", loader=self.loader)

    def query(self, query: str):
        if not query:
            return "Query must Not be Empty!"
        response = self.app.query(query)
        return response
