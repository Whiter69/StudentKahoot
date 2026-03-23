from certifi import contents
from flask import Flask,jsonify,request
import random

app=Flask(__name__)

ACTIVE_GAMES={}

@app.route('/create_room',methods=['GET','POST'])
def create_room():
    data=request.json
    host_nick=data.get("host")
    pin=str(random.randint(1000,9999))
    ACTIVE_GAMES[pin]={
        "status":"waiting",
        "host":host_nick,
        "players":[host_nick]
    }
    print(f"Serwer utworzył nowy pokój: {pin}")
    return jsonify({"sukces":True,"pin":pin})
@app.route('/',methods=['GET'])
def get_active_games():
    return jsonify(ACTIVE_GAMES)

@app.route('/join_room',methods=['GET','POST'])
def join_room():
    data=request.json
    pin=data.get("pin")
    nick=data.get("nick")

    if pin in ACTIVE_GAMES:
        ACTIVE_GAMES[pin]["players"].append(nick)
        print(f"Gracz {nick} dołączył do pokoju {pin}")
        return jsonify({"sukces":True,"message":"Dołączyłeś do pokoju!"})
    else:
        return jsonify({"sukces":False,"message":"Nie znaleziono pokoju"})

@app.route('/choose_category',methods=['GET','POST'])
def choose_category():
    data=request.json
    pin=data.get("pin")
    category=data.get("category")


    if pin in ACTIVE_GAMES:
        ACTIVE_GAMES[pin]["category"]=category
        ACTIVE_GAMES[pin]["status"]="question"
        ACTIVE_GAMES[pin]["current_question"]={"question_content":"Pierwsze pytanie","answers":[]}
        print(f"Kategoria {category} została wybrana dla pokoju {pin}")
        return jsonify({"sukces":True,"message":"Kategoria została wybrana!"})
    else:
        return jsonify({"sukces":False,"message":"Nie znaleziono pokoju"})


@app.route('/room_status/<pin>',methods=['GET'])
def room_status(pin):
    if pin in ACTIVE_GAMES:
        return jsonify({"sukces":True,"status":ACTIVE_GAMES[pin]["status"],"players":ACTIVE_GAMES[pin]["players"],"host":ACTIVE_GAMES[pin]["host"]})
    else:
        return jsonify({"sukces":False,"message":"Nie znaleziono pokoju"})

if __name__=="__main__":
    app.run(debug=True)