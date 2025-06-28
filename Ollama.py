import requests
import json


class Ollama:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.headers = {"Content-Type": "application/json"}
        self.model = "mistral"

    def generateAnswer(self, prompt):
        prompt = ("Bitte antworte nur mit den Programmiersprachen die in  "
                  "dem Job gefordert werden" + prompt)
        data = {"model": self.model,
                "prompt": prompt,
                "stream": False}
        response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            response_text = response.text
            data = json.loads(response_text)
            actual_response = self.formatAnswer(data["response"])
        else:
            raise Exception("Error generating answer")
        return actual_response

    def formatAnswer(self, prompt):
        prompt = prompt + " lösche hier alle füllwörter raus und gib mir eine Antowrt in der Art Java, Html, Go. Also BITTE NUR DIE PROGRAMMIERSPRACHEN OHNE JEGLICHE BESCHREIBUNGEN ZU DIESEN"
        data = {"model": self.model,
                "prompt": prompt,
                "stream": False}
        response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            response_text = response.text
            data = json.loads(response_text)
            actual_response = data["response"]
        else:
            raise Exception("Error generating answer")
        return actual_response
