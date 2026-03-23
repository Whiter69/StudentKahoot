import requests

SERVER_URL="http://127.0.0.1:5000"

def make_new_room(host):
    try:
        response=requests.post(f"{SERVER_URL}/create_room",json={"host":host})
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

def check_room_status(pin):
    try:
        response=requests.get(f"{SERVER_URL}/room_status/{pin}")
        data=response.json()
        return data
    except Exception as e:
        print(f"Nie można połączyć się z serwerem: {e}")
        return {"sukces": False, "message": "Błąd połączenia z serwerem"}

def send_category(pin,category):
    try:
        response=requests.post(f"{SERVER_URL}/choose_category",json={"pin":pin,"category":category})
        data=response.json()
        return data
    except Exception as e:
        print(f"Nie można połączyć się z serwerem: {e}")
        return {"sukces": False, "message": "Błąd połączenia z serwerem"}