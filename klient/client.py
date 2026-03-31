from multiprocessing.connection import answer_challenge

import customtkinter as ctk
import api_siec

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.geometry("800x600")
app.title("Quiz-Klient")


my_nick = ""
my_pin = ""

nick_entry = None
pin_entry = None
making_game_info = None
making_game_info_2 = None


def clear_screen():
    for widget in app.winfo_children():
        widget.grid_forget()

def loop_radar():

    if my_pin != "":
        response = api_siec.check_room_status(my_pin)
        if response:
            players = len(response.get("players", []))
            host_name = response.get("host")

            if players == 1:
                making_game_info_2.configure(text=f"Czekanie na drugiego gracza 1/2", text_color="green")
            elif players == 2:
                category_screen(host_name)
                return

        app.after(1000, loop_radar)

def show_lobby_screen():
    global nick_entry, pin_entry, making_game_info, making_game_info_2

    clear_screen()
    app.grid_columnconfigure(0, weight=1)

    title = ctk.CTkLabel(app, text="Witaj w Quizie!", font=("Arial", 44, "bold"))
    title.grid(row=0, column=0, pady=(40, 0), padx=10)

    nick_entry = ctk.CTkEntry(app, placeholder_text="Twoja nazwa", width=200, height=30, text_color="#000000",
                              font=("Helvetica", 16))
    nick_entry.grid(row=1, column=0, pady=(20, 10), padx=20)

    button_stworz = ctk.CTkButton(app, text="Stwórz nowy pokój", command=click_stworz_gre, height=40,
                                  text_color="#000000", font=("Helvetica", 16, "bold"))
    button_stworz.grid(row=2, column=0, pady=20)

    pin_entry = ctk.CTkEntry(app, placeholder_text="PIN do gry", width=200, height=30, text_color="#000000",
                             font=("Helvetica", 16))
    pin_entry.grid(row=3, column=0, pady=(20, 10), padx=20)

    button_dolacz = ctk.CTkButton(app, text="Dołącz do gry", command=click_dolacz_do_gry, height=40,
                                  text_color="#000000", font=("Helvetica", 16, "bold"))
    button_dolacz.grid(row=4, column=0, pady=20)

    making_game_info = ctk.CTkLabel(app, text="", font=("Arial", 18))
    making_game_info.grid(row=5, column=0, pady=20, padx=20)

    making_game_info_2 = ctk.CTkLabel(app, text="", font=("Arial", 18))
    making_game_info_2.grid(row=6, column=0, pady=20, padx=20)

def click_dolacz_do_gry():
    global my_nick, my_pin
    player = nick_entry.get()
    pin = pin_entry.get()

    if player == "" or pin == "":
        making_game_info.configure(text="Podaj swoją nazwę i PIN!", text_color="red")
        return

    making_game_info.configure(text="Łączenie z serwerem...", text_color="green")
    app.update()

    sukces, message = api_siec.join_room(pin, player)

    if sukces:
        making_game_info.configure(text=message, text_color="green")
        my_nick = player
        my_pin = pin
        loop_radar()
    else:
        making_game_info.configure(text=message, text_color="red")

def click_stworz_gre():
    global my_nick, my_pin
    player = nick_entry.get()

    if player == "":
        making_game_info.configure(text="Podaj swoją nazwę!", text_color="red")
        return

    making_game_info.configure(text="Łączenie z serwerem...", text_color="green")
    app.update()

    generated_pin = api_siec.make_new_room(player)
    my_nick = player
    my_pin = generated_pin

    making_game_info.configure(text=f"Twój PIN do gry to: {generated_pin}", text_color="green")
    loop_radar()




def category_screen(host_name):
    clear_screen()

    title = ctk.CTkLabel(app, text="Wybór Kategorii", font=("Arial", 44, "bold"))
    title.grid(row=0, column=0, pady=(40, 20))


    if my_nick == host_name:
        info = ctk.CTkLabel(app, text="Jesteś Hostem! Wybierz kategorię:", font=("Arial", 20), text_color="lightblue")
        info.grid(row=1, column=0, pady=10)

        cat1_button = ctk.CTkButton(app, text="Podstawy Programowania",command=lambda: choosen_category("Podstawy Programowania"),font=("Arial", 30),text_color="#040005")
        cat1_button.grid(row=2, column=0, pady=20)

        cat2_button = ctk.CTkButton(app, text="Bazy danych",command=lambda: choosen_category("Bazy danych"), font=("Arial", 30), text_color="#040005")
        cat2_button.grid(row=3, column=0, pady=20)

        cat3_button = ctk.CTkButton(app, text="Sztuczna Inteligencja",command=lambda: choosen_category("Sztuczna Inteligencja"), font=("Arial", 30), text_color="#040005")
        cat3_button.grid(row=4, column=0, pady=20)

        cat4_button = ctk.CTkButton(app, text="Cyberbezpieczeństwo",command=lambda: choosen_category("Cyberbezpieczeństwo"), font=("Arial", 30), text_color="#040005")
        cat4_button.grid(row=5, column=0, pady=20)

    else:
        info = ctk.CTkLabel(app, text="Czekaj, aż Host wybierze kategorię...", font=("Arial", 20), text_color="orange")
        info.grid(row=1, column=0, pady=10)
    question_radar()


def choosen_category(category):
    loading_screen()
    app.update()
    api_siec.send_category(my_pin, category)
    api_siec.get_question(my_pin)

def loading_screen():
    clear_screen()
    loading_label = ctk.CTkLabel(app, text="Generowanie pytania....", font=("Arial", 24))
    loading_label.grid(row=0, column=0, pady=20)

def question_radar():
    if my_pin != "":
        response=api_siec.check_room_status(my_pin)
        if response.get("status")=="question":
            question=response.get("current_question")
            question_screen(question)
            return
        app.after(1000, question_radar)

def question_screen(question):
    clear_screen()
    correct_ans = question["correct_answer"]

    question_label = ctk.CTkLabel(app, text=question["question_content"], font=("Arial", 24), wraplength=600)
    question_label.grid(row=0, column=0, pady=20)

    answer1_button = ctk.CTkButton(app, text=question["answers"][0], font=("Arial", 20), text_color="#040005",
                                   command=lambda: check_answer(question["answers"][0], correct_ans))
    answer1_button.grid(row=1, column=0, pady=10)

    answer2_button = ctk.CTkButton(app, text=question["answers"][1], font=("Arial", 20), text_color="#040005",
                                   command=lambda: check_answer(question["answers"][1], correct_ans))
    answer2_button.grid(row=2, column=0, pady=10)

    answer3_button = ctk.CTkButton(app, text=question["answers"][2], font=("Arial", 20), text_color="#040005",
                                   command=lambda: check_answer(question["answers"][2], correct_ans))
    answer3_button.grid(row=3, column=0, pady=10)

    answer4_button = ctk.CTkButton(app, text=question["answers"][3], font=("Arial", 20), text_color="#040005",
                                   command=lambda: check_answer(question["answers"][3], correct_ans))
    answer4_button.grid(row=4, column=0, pady=10)
show_lobby_screen()


def check_answer(choosen_ans, correct_ans):
    clear_screen()
    if choosen_ans== correct_ans:
        wynik_label = ctk.CTkLabel(app, text="Brawo! Poprawna odpowiedź!", font=("Arial", 34, "bold"),
                                   text_color="green")
        wynik_label.grid(row=0, column=0, pady=100)
    else:
        wynik_label = ctk.CTkLabel(app, text="Niestety, źle!", font=("Arial", 34, "bold"), text_color="red")
        wynik_label.grid(row=0, column=0, pady=(100, 20))

        correct_label = ctk.CTkLabel(app, text=f"Poprawna odpowiedź to:\n{correct_ans}", font=("Arial", 20))
        correct_label.grid(row=1, column=0, pady=10)

if __name__ == "__main__":
    app.mainloop()