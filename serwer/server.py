import json
import random
import sqlite3
from flask import Flask, jsonify, request
from google import genai


class QuizServer:
    def __init__(self, api_key):
        self.app = Flask(__name__)
        self.ai_client = genai.Client(api_key=api_key)
        self.active_games = {}

        self.app.add_url_rule('/create_room', 'create_room', self.create_room, methods=['GET', 'POST'])
        self.app.add_url_rule('/', 'get_active_games', self.get_active_games, methods=['GET'])
        self.app.add_url_rule('/join_room', 'join_room', self.join_room, methods=['GET', 'POST'])
        self.app.add_url_rule('/choose_category', 'choose_category', self.choose_category, methods=['GET', 'POST'])
        self.app.add_url_rule('/send_question', 'send_question', self.send_question, methods=['POST'])
        self.app.add_url_rule('/check_answer', 'check_answer', self.check_answer, methods=['GET', 'POST'])
        self.app.add_url_rule('/room_status/<pin>', 'room_status', self.room_status, methods=['GET'])
        self.app.add_url_rule('/next_round', 'next_round', self.next_round, methods=['POST'])

    def create_room(self):
        data = request.json
        host_nick = data.get("host")
        pin = str(random.randint(1000, 9999))
        self.active_games[pin] = {
            "status": "waiting",
            "host": host_nick,
            "players": [host_nick],
            "scores": {host_nick: 0},
            "current_round": 1,
            "asked_questions": []
        }
        print(f"Serwer utworzył nowy pokój: {pin}")
        return jsonify({"sukces": True, "pin": pin})

    def get_active_games(self):
        return jsonify(self.active_games)

    def join_room(self):
        data = request.json
        pin = data.get("pin")
        nick = data.get("nick")

        if pin in self.active_games:
            self.active_games[pin]["players"].append(nick)
            self.active_games[pin]["scores"][nick] = 0
            print(f"Gracz {nick} dołączył do pokoju {pin}")
            return jsonify({"sukces": True, "message": "Dołączyłeś do pokoju!"})
        else:
            return jsonify({"sukces": False, "message": "Nie znaleziono pokoju"})

    def choose_category(self):
        data = request.json
        pin = data.get("pin")
        category = data.get("category")

        if pin in self.active_games:
            self.active_games[pin]["category"] = category
            self.active_games[pin]["status"] = "generating_question"
            print(f"Kategoria {category} została wybrana dla pokoju {pin}")
            return jsonify({"sukces": True, "message": "Kategoria została wybrana!"})
        else:
            return jsonify({"sukces": False, "message": "Nie znaleziono pokoju"})

    def send_question(self):
        data = request.json
        pin = data.get("pin")

        if pin not in self.active_games:
            return jsonify({"sukces": False, "message": "Nie znaleziono pokoju"})

        category = self.active_games[pin]["category"]
        history = self.active_games[pin]["asked_questions"]
        history_text = ", ".join(history) if history else "Brak"

        try:
            prompt = f"""
               Jesteś profesjonalnym generatorem quizów. Wygeneruj 1 proste pytanie z kategorii: {category}.
               ZAKAZ POWTÓREK: NIE WOLNO Ci użyć tych pytań: {history_text}.
               Zwróć odpowiedź TYLKO w formacie JSON:
               {{
                   "question_content": "Treść pytania",
                   "answers": ["Odp A", "Odp B", "Odp C", "Odp D"],
                   "correct_answer": "Odp A"
               }}
               Nie dodawaj żadnego tekstu, tylko JSON.
               """
            response = self.ai_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            clear_text = response.text.replace('```json', '').replace('```', '').strip()
            generated_question = json.loads(clear_text)

            try:
                conn = sqlite3.connect("quiz_baza.db")
                cursor = conn.cursor()

                question_content = generated_question["question_content"]
                cursor.execute("SELECT id FROM pytania WHERE tresc = ?", (question_content,))
                exists = cursor.fetchone()

                if not exists:
                    ans = generated_question["answers"]
                    correct = generated_question["correct_answer"]

                    cursor.execute('''
                                   INSERT INTO pytania (kategoria, tresc, odp_a, odp_b, odp_c, odp_d, poprawna)
                                   VALUES (?, ?, ?, ?, ?, ?, ?)
                                   ''', (category, question_content, ans[0], ans[1], ans[2], ans[3], correct))

                    conn.commit()
                    print(f"[BAZA] Zapisano nowe pytanie od AI do bazy! Tresc: '{question_content[:30]}...'")

                conn.close()
            except Exception as e:
                print(f"Błąd podczas dodawania pytania AI do bazy: {e}")

            self.active_games[pin]["current_question"] = generated_question
            self.active_games[pin]["status"] = "question"
            self.active_games[pin]["asked_questions"].append(generated_question["question_content"])

            print(f"Pytanie (AI) wysłane do pokoju {pin}")
            return jsonify({"sukces": True, "question": generated_question})

        except Exception as e:
            print(f"Błąd API Google: {e}. Przełączam na BAZĘ DANYCH SQLite!")

            try:
                conn = sqlite3.connect("quiz_baza.db")
                cursor = conn.cursor()

                cursor.execute("SELECT tresc, odp_a, odp_b, odp_c, odp_d, poprawna FROM pytania WHERE kategoria = ?",
                               (category,))
                all_questions = cursor.fetchall()
                conn.close()

                available = []
                for row in all_questions:
                    content = row[0]
                    if content not in history:
                        available.append({
                            "question_content": content,
                            "answers": [row[1], row[2], row[3], row[4]],
                            "correct_answer": row[5]
                        })

                if available:
                    selected_questions = random.choice(available)

                    random.shuffle(selected_questions["answers"])

                    self.active_games[pin]["current_question"] = selected_questions
                    self.active_games[pin]["status"] = "question"
                    self.active_games[pin]["asked_questions"].append(selected_questions["question_content"])

                    print(f"Pobrano pytanie z BAZY dla kategorii: {category}")
                    return jsonify({"sukces": True, "question": selected_questions})
                else:
                    self.active_games[pin]["status"] = "waiting"
                    return jsonify({"sukces": False, "message": "Brak nowych pytań w bazie."})

            except Exception as db_err:
                print(f"BŁĄD BAZY DANYCH: {db_err}")
                self.active_games[pin]["status"] = "waiting"
                return jsonify({"sukces": False, "message": "Błąd krytyczny: Brak AI i błąd bazy!"})

    def check_answer(self):
        data = request.json
        pin = data.get("pin")
        answer = data.get("answer")
        nick = data.get("nick")

        if pin not in self.active_games:
            return jsonify({"sukces": False, "message": "Nie znaleziono pokoju"})

        current_question = self.active_games[pin].get("current_question")

        if current_question is None:
            return jsonify({"sukces": False, "message": "Runda już się zakończyła!"})

        correct_answer = current_question.get("correct_answer")

        if not correct_answer:
            return jsonify({"sukces": False, "message": "Brak poprawnej odpowiedzi w strukturze pytania"})

        if answer == correct_answer:
            self.active_games[pin]["scores"][nick] += 1
            return jsonify({"sukces": True, "message": "Poprawna odpowiedź!"})
        else:
            return jsonify({"sukces": True, "message": f"Niepoprawna odpowiedź! Poprawna to: {correct_answer}"})
    def next_round(self):
        data = request.json
        pin = data.get("pin")

        if pin in self.active_games:
            self.active_games[pin]["current_round"] += 1
            self.active_games[pin]["current_question"] = None

            if self.active_games[pin]["current_round"] > 7:
                self.active_games[pin]["status"] = "results"

                try:
                    category= self.active_games[pin].get("category", "Nieznana")
                    conn = sqlite3.connect("quiz_baza.db")
                    cursor = conn.cursor()

                    cursor.execute("INSERT INTO mecze (pin, kategoria) VALUES (?, ?)", (pin, category))
                    game_id = cursor.lastrowid

                    for player, points in self.active_games[pin]["scores"].items():
                        cursor.execute("INSERT INTO wyniki (mecz_id, gracz, punkty) VALUES (?, ?, ?)",
                                       (game_id, player, points))

                    conn.commit()
                    conn.close()
                    print(f"--- ZAPISANO WYNIKI MECZU '{pin}' DO BAZY! ---")
                except Exception as e:
                    print(f"Błąd podczas zapisu meczu do bazy: {e}")

                return jsonify({"sukces": True, "status": "results"})
            else:
                self.active_games[pin]["status"] = "generating_question"
                return jsonify({"sukces": True, "status": "continue"})

        return jsonify({"sukces": False})

    def room_status(self, pin):
        if pin in self.active_games:
            return jsonify({
                "sukces": True,
                "status": self.active_games[pin]["status"],
                "players": self.active_games[pin]["players"],
                "host": self.active_games[pin]["host"],
                "current_question": self.active_games[pin].get("current_question"),
                "scores": self.active_games[pin].get("scores", {}),
                "current_round": self.active_games[pin].get("current_round", 1)
            })
        else:
            return jsonify({"sukces": False, "message": "Nie znaleziono pokoju"})

    def run(self):
        self.app.run('0.0.0.0',port=5000,debug=True)


if __name__ == "__main__":
    GEMINI_KEY = "klucz"
    server = QuizServer(api_key=GEMINI_KEY)
    server.run()