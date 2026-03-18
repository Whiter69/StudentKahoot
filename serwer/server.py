
from flask import Flask,jsonify,request
import random

app=Flask(__name__)

ACTIVE_GAMES={}

@app.route('/create_room',methods=['GET','POST'])
def create_room():

    pin=str(random.randint(1000,9999))
    ACTIVE_GAMES[pin]={
        "status":"waiting",
        "players":[]
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


if __name__=="__main__":
    app.run(debug=True)