import json


class ConfigParser(dict):
    def __init__(self, file):
        super().__init__()
        self.file = file
        with open(self.file) as f:
            self.update(json.load(f))

    def save(self):
        with open(self.file, 'w') as f:
            json.dump(self, f, indent=4)
            f.write('\n')
