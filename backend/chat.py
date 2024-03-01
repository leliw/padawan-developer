import json


class Chat:
    def __init__(self):
        with open("chat.json", "tr", encoding="utf-8") as file:
            self.data = json.load(file)

    def get_answer(self, question):
        commands = self.data.get(question)
        if commands:
            return "\n".join([c["command"] for c in commands])
        return "I don't understand you"
