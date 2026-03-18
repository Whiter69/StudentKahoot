import requests

SERVER_URL="http://127.0.0.1:5000"

def make_new_room():
    try:
        response=requests.post(f"{SERVER_URL}/create_room")
        data=response.json()
        return data.get("pin")
    except Exception as e:
        print(f"Nie można połączyć się z serwerem: {e}")

def join_room(pin,nick):
    try:
        response=requests.post(f"{SERVER_URL}/join_room",json={"pin":pin,"nick":nick})
        data=response.json()
        return data.get("sukces"),data.get("message")
    except Exception as e:
        print(f"Nie można połączyć się z serwerem: {e}")
        return False,"Błąd połączenia z serwerem"