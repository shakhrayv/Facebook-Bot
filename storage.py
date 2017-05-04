import json


class Storage:
    def __init__(self):
        self.load()

    def auth(self, sender):
        if sender not in self.data.keys():
            self.data[sender] = {}

    def save(self):
        file = open("data.json", 'w')
        file.write(json.dumps(self.data))
        file.close()

    def load(self):
        try:
            file = open("data.json", 'r')
            self.data = json.loads(file.read())
        except:
            self.data = {}

    def save_text(self, sender, text, title="Untitled"):
        self.auth(sender)
        self.data[sender][title] = text
        self.save()

    def load_text(self, sender, title):
        self.auth(sender)
        if title in self.data[sender].keys():
            return self.data[sender][title]
        return ''

    def share_text(self, sender, title):
        self.auth(sender)
        if title in self.data[sender].keys():
            for s in self.data.keys():
                self.data[s][title] = self.data[sender][title]
        self.save()

    def titles(self, sender):
        self.auth(sender)
        return self.data[sender].keys()

    def clear(self, sender):
        self.auth(sender)
        self.data[sender] = {}