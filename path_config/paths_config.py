import json

class PathConfig:
    def __init__(self):
        self.read_config()

    def path(self,file):
        return self.data[file]
    
    def read_config(self):
        with open('config.json') as json_:
            self.data = json.load(json_)
