import requests

class QuizAPIClient:
    def __init__(self, server_url="http://127.0.0.1:5000"):
        self.server_url = server_url

    def make_new_room(self, host):
        try:
            response = requests.post(f"{self.server_url}/create_room", json={"host": host})
            data = response.json()
            return data.get("pin")
        except Exception as e:
            print(f"Nie można połączyć się z serwerem: {e}")

    def join_room(self, pin, nick):
        try:
            response = requests.post(f"{self.server_url}/join_room", json={"pin": pin, "nick": nick})
            return response.json()
        except Exception as e:
            print(f"Nie można połączyć się z serwerem: {e}")
            return {"sukces": False, "message": "Błąd połączenia z serwerem"}

    def check_room_status(self, pin):
        try:
            response = requests.get(f"{self.server_url}/room_status/{pin}")
            return response.json()
        except Exception as e:
            print(f"Nie można połączyć się z serwerem: {e}")
            return {"sukces": False, "message": "Błąd połączenia z serwerem"}

    def send_category(self, pin, category):
        try:
            response = requests.post(f"{self.server_url}/choose_category", json={"pin": pin, "category": category})
            data = response.json()
            return data.get("sukces"), data.get("message")
        except Exception as e:
            print(f"Nie można połączyć się z serwerem: {e}")
            return False, "Błąd połączenia z serwerem"

    def get_question(self, pin):
        try:
            response = requests.post(f"{self.server_url}/send_question", json={"pin": pin})
            return response.json()
        except Exception as e:
            print(f"Nie można połączyć się z serwerem: {e}")
            return {"sukces": False, "message": "Błąd połączenia z serwerem"}

    def check_answer(self, pin, answer, nick):
        try:
            response = requests.post(f"{self.server_url}/check_answer", json={"pin": pin, "answer": answer, "nick": nick})
            return response.json()
        except Exception as e:
            print(f"Nie można połączyć się z serwerem: {e}")
            return {"sukces": False, "message": "Błąd połączenia z serwerem"}

    def next_round(self, pin):
        try:
            response = requests.post(f"{self.server_url}/next_round", json={"pin": pin})
            return response.json()
        except Exception as e:
            print(f"Błąd: {e}")
            return {"sukces": False}