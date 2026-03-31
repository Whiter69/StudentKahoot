import json

from certifi import contents
from flask import Flask,jsonify,request
import random
from google import genai

GEMINI_KEY="AIzaSyBxbZCBOyMNMDPhGkhnPLev7kSQ_elTv7U"
app=Flask(__name__)
ai_client=genai.Client(api_key=GEMINI_KEY)

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
        ACTIVE_GAMES[pin]["status"]="genertaing_question"
        print(f"Kategoria {category} została wybrana dla pokoju {pin}")
        return jsonify({"sukces":True,"message":"Kategoria została wybrana!"})
    else:
        return jsonify({"sukces":False,"message":"Nie znaleziono pokoju"})


@app.route('/send_question', methods=['POST'])
def send_question():
    data = request.json
    pin = data.get("pin")

    if pin not in ACTIVE_GAMES:
        return jsonify({"sukces": False, "message": "Nie znaleziono pokoju"})
    category = ACTIVE_GAMES[pin]["category"]
    try:
        prompt = f"""
           Wygeneruj 1 pytanie quizowe z kategorii: {category}.
           Zwróć odpowiedź TYLKO w czystym formacie JSON o takiej strukturze:
           {{
               "question_content": "Treść Twojego pytania",
               "answers": ["Odp A", "Odp B", "Odp C", "Odp D"],
               "correct_answer": "Odp A"
           }}
           Nie dodawaj żadnego innego tekstu, tylko sam JSON.
           """
        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        clear_text = response.text.replace('```json', '').replace('```', '').strip()
        generated_question = json.loads(clear_text)

        ACTIVE_GAMES[pin]["current_question"] = generated_question
        ACTIVE_GAMES[pin]["status"] ="question"
        print(f"Pytanie z {category} zostało wysłane do pokoju {pin}")
        return jsonify({"sukces": True, "question": generated_question})
    except Exception as e:
        print(f"Błąd podczas generowania AI: {e}")
        return jsonify({"sukces": False, "message": "Błąd generowania pytania przez AI"})

@app.route('/check_answer',methods=['GET','POST'])
def check_answer():
    data=request.json
    pin=data.get("pin")
    answer=data.get("answer")
    if pin not in ACTIVE_GAMES:
        return jsonify({"sukces": False, "message": "Nie znaleziono pokoju"})
    correct_answer=ACTIVE_GAMES[pin].get("current_question",{}).get("correct_answer")
    if not correct_answer:
        return jsonify({"sukces": False, "message": "Brak aktywnego pytania"})
    if answer==correct_answer:
        return jsonify({"sukces": True, "message": "Poprawna odpowiedź!"})
    else:
        return jsonify({"sukces": True, "message": f"Niepoprawna odpowiedź! Poprawna to: {correct_answer}"})
@app.route('/room_status/<pin>',methods=['GET'])
def room_status(pin):
    if pin in ACTIVE_GAMES:
        return jsonify({"sukces":True,
                        "status":ACTIVE_GAMES[pin]["status"]
                           ,"players":ACTIVE_GAMES[pin]["players"]
                           ,"host":ACTIVE_GAMES[pin]["host"]
                            ,"current_question":ACTIVE_GAMES[pin].get("current_question")})
    else:
        return jsonify({"sukces":False,"message":"Nie znaleziono pokoju"})

if __name__=="__main__":
    app.run(debug=True)