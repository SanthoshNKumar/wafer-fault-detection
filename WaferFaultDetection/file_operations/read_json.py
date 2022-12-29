import json

class GetJsonData:
    def __init__(self):
        #self.path = path
        self.configfile = "config.json"

    def read_data_json(self, varible):
        with open(self.configfile, 'r') as f:
            dic = json.load(f)
            f.close()

        pattern = dic[varible]

        return pattern
