import json


class Config:

    def __init__(self):

        with open("settings.json", "r") as file:
            self.data = json.load(file)

    def get(self, section, key):

        return self.data[section][key]

    def set(self, section, key, value):

        self.data[section][key] = value

        with open("settings.json", "w") as file:

            json.dump(self.data, file, indent=4)