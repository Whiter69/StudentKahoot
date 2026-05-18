import customtkinter as ctk
import threading
from api_siec import QuizAPIClient



class QuizApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("900x700")
        self.title("Kahoot AI")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.api = QuizAPIClient()


        self.my_nick = ""
        self.my_pin = ""
        self.my_current_round = 0
        self.timer_event = None


        self.show_main_menu()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.pack_forget()
            widget.grid_forget()
            widget.place_forget()


    def show_main_menu(self):
        self.clear_screen()

        title = ctk.CTkLabel(self, text="K A H O O T   A I", font=("Arial", 50, "bold"), text_color="#2ECC71")
        title.pack(pady=(100, 60))

        btn_create = ctk.CTkButton(self, text="Stwórz nową grę", font=("Arial", 24, "bold"), height=60, width=350,
                                   command=self.show_create_room)
        btn_create.pack(pady=15)

        btn_join = ctk.CTkButton(self, text="Dołącz do gry", font=("Arial", 24, "bold"), height=60, width=350,
                                 fg_color="#3498DB", hover_color="#2980B9", command=self.show_join_room)
        btn_join.pack(pady=15)

        btn_exit = ctk.CTkButton(self, text="Wyjdź", font=("Arial", 24, "bold"), height=60, width=350,
                                 fg_color="#E74C3C", hover_color="#C0392B", command=self.destroy)
        btn_exit.pack(pady=15)

    def show_create_room(self):
        self.clear_screen()

        title = ctk.CTkLabel(self, text="Stwórz Pokój", font=("Arial", 40, "bold"))
        title.pack(pady=(80, 40))

        self.nick_entry = ctk.CTkEntry(self, placeholder_text="Podaj swój Nick", width=350, height=50,
                                       font=("Arial", 20), justify="center")
        self.nick_entry.pack(pady=20)

        btn_create = ctk.CTkButton(self, text="Utwórz", font=("Arial", 24, "bold"), height=50, width=350,
                                   command=self.click_stworz_gre)
        btn_create.pack(pady=20)

        self.making_game_info = ctk.CTkLabel(self, text="", font=("Arial", 18))
        self.making_game_info.pack(pady=10)


        btn_back = ctk.CTkButton(self, text="Wróć", font=("Arial", 18), fg_color="transparent", border_width=2,
                                 hover_color="#34495E", command=self.show_main_menu)
        btn_back.pack(pady=40)


    def show_join_room(self):
        self.clear_screen()

        title = ctk.CTkLabel(self, text="Dołącz do gry", font=("Arial", 40, "bold"))
        title.pack(pady=(80, 40))

        self.nick_entry = ctk.CTkEntry(self, placeholder_text="Podaj swój Nick", width=350, height=50,
                                       font=("Arial", 20), justify="center")
        self.nick_entry.pack(pady=15)

        self.pin_entry = ctk.CTkEntry(self, placeholder_text="Podaj kod PIN", width=350, height=50, font=("Arial", 20),
                                      justify="center")
        self.pin_entry.pack(pady=15)

        btn_join = ctk.CTkButton(self, text="Wejdź do gry", font=("Arial", 24, "bold"), height=50, width=350,
                                 fg_color="#3498DB", hover_color="#2980B9", command=self.click_dolacz_do_gry)
        btn_join.pack(pady=20)

        self.making_game_info = ctk.CTkLabel(self, text="", font=("Arial", 18))
        self.making_game_info.pack(pady=10)


        btn_back = ctk.CTkButton(self, text="Wróć", font=("Arial", 18), fg_color="transparent", border_width=2,
                                 hover_color="#34495E", command=self.show_main_menu)
        btn_back.pack(pady=20)

    def click_stworz_gre(self):
        player = self.nick_entry.get()
        if player == "":
            self.making_game_info.configure(text="Podaj swoją nazwę!", text_color="red")
            return

        self.making_game_info.configure(text="Tworzenie serwera...", text_color="#F1C40F")
        self.update()

        generated_pin = self.api.make_new_room(player)
        self.my_nick = player
        self.my_pin = generated_pin

        self.show_waiting_screen(f"Twój PIN do gry to:\n\n{generated_pin}\n\nOczekuję na gracza...")
        self.loop_radar()

    def click_dolacz_do_gry(self):
        player = self.nick_entry.get()
        pin = self.pin_entry.get()

        if player == "" or pin == "":
            self.making_game_info.configure(text="Wypełnij wszystkie pola!", text_color="red")
            return

        self.making_game_info.configure(text="Łączenie...", text_color="#F1C40F")
        self.update()

        response = self.api.join_room(pin, player)

        if response.get("sukces"):
            self.my_nick = player
            self.my_pin = pin
            self.show_waiting_screen("Udało się dołączyć!\n\nCzekaj, aż Host wybierze kategorię...")
            self.loop_radar()
        else:
            self.making_game_info.configure(text=response.get("message"), text_color="red")

    def show_waiting_screen(self, message):
        self.clear_screen()
        info_label = ctk.CTkLabel(self, text=message, font=("Arial", 30, "bold"), text_color="#3498DB")
        info_label.pack(expand=True)

    def loop_radar(self):
        if self.my_pin != "":
            response = self.api.check_room_status(self.my_pin)
            if response:
                players = len(response.get("players", []))
                host_name = response.get("host")

                if players == 2:
                    self.category_screen(host_name)
                    return

            self.after(1000, self.loop_radar)


    def category_screen(self, host_name):
        self.clear_screen()
        title = ctk.CTkLabel(self, text="Wybierz Dziedzinę", font=("Arial", 44, "bold"))
        title.pack(pady=(40, 10))

        if self.my_nick == host_name:
            info = ctk.CTkLabel(self, text="Jesteś Hostem! Rozpocznij grę.", font=("Arial", 20), text_color="#BDC3C7")
            info.pack(pady=10)

            # Ramka na przyciski kategorii w siatce 2x2
            cat_frame = ctk.CTkFrame(self, fg_color="transparent")
            cat_frame.pack(pady=20, padx=40, fill="both", expand=True)

            cat_frame.grid_columnconfigure(0, weight=1)
            cat_frame.grid_columnconfigure(1, weight=1)

            categories = ["Podstawy Programowania", "Bazy danych", "Sztuczna Inteligencja", "Cyberbezpieczeństwo"]
            colors = ["#9B59B6", "#E67E22", "#1ABC9C", "#34495E"]

            for idx, cat in enumerate(categories):
                r, c = idx // 2, idx % 2
                btn = ctk.CTkButton(cat_frame, text=cat, command=lambda c=cat: self.choosen_category(c),
                                    font=("Arial", 24, "bold"), fg_color=colors[idx], height=100, corner_radius=15)
                btn.grid(row=r, column=c, padx=15, pady=15, sticky="nsew")
        else:
            self.show_waiting_screen("Czekaj, aż Host wybierze kategorię...")

        self.question_radar()

    def choosen_category(self, category):
        self.loading_screen()
        self.update()
        self.api.send_category(self.my_pin, category)

        def fetch_q():
            self.api.get_question(self.my_pin)

        threading.Thread(target=fetch_q).start()

    def loading_screen(self):
        self.clear_screen()
        loading_label = ctk.CTkLabel(self, text="AI wymyśla pytanie...", font=("Arial", 36, "bold"),
                                     text_color="#F1C40F")
        loading_label.pack(expand=True)


    def question_radar(self):
        if self.my_pin != "":
            response = self.api.check_room_status(self.my_pin)
            if response:
                status = response.get("status")
                server_round = response.get("current_round", 1)

                if status == "question" and server_round > self.my_current_round:
                    question = response.get("current_question")
                    self.question_screen(question, server_round)
                    return
                elif status == "results":
                    self.results_screen(response.get("scores", {}))
                    return

            self.after(1000, self.question_radar)

    def result_radar(self):
        if self.my_pin != "":
            response = self.api.check_room_status(self.my_pin)
            if response:
                status = response.get("status")
                server_round = response.get("current_round", 1)

                if status == "generating_question":
                    self.loading_screen()
                    self.question_radar()
                    return
                elif status == "question" and server_round > self.my_current_round:
                    question = response.get("current_question")
                    self.question_screen(question, server_round)
                    return
                elif status == "results":
                    self.results_screen(response.get("scores", {}))
                    return

            self.after(1000, self.result_radar)


    def question_screen(self, question, current_round):
        self.my_current_round = current_round
        self.clear_screen()
        correct_ans = question["correct_answer"]
        time_left = 15


        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=40, pady=(20, 0))

        round_label = ctk.CTkLabel(top_bar, text=f"Pytanie {current_round} z 7", font=("Arial", 20, "bold"),
                                   text_color="#BDC3C7")
        round_label.pack(side="left")

        self.timer_label = ctk.CTkLabel(top_bar, text=f"⏱ {time_left}s", font=("Arial", 28, "bold"),
                                        text_color="#E74C3C")
        self.timer_label.pack(side="right")

        q_frame = ctk.CTkFrame(self, fg_color="#ECF0F1", corner_radius=15)
        q_frame.pack(pady=20, padx=40, fill="x")

        q_label = ctk.CTkLabel(q_frame, text=question["question_content"], font=("Arial", 24, "bold"),
                               text_color="#2C3E50", wraplength=750)
        q_label.pack(pady=40, padx=20)

        ans_frame = ctk.CTkFrame(self, fg_color="transparent")
        ans_frame.pack(pady=10, padx=40, fill="both", expand=True)

        ans_frame.grid_columnconfigure(0, weight=1)
        ans_frame.grid_columnconfigure(1, weight=1)
        ans_frame.grid_rowconfigure(0, weight=1)
        ans_frame.grid_rowconfigure(1, weight=1)

        kahoot_colors = [("#E74C3C", "#C0392B"), ("#3498DB", "#2980B9"), ("#F1C40F", "#F39C12"), ("#2ECC71", "#27AE60")]

        import textwrap

        for idx, ans in enumerate(question["answers"]):
            r, c = idx // 2, idx % 2
            bg_color, hover_color = kahoot_colors[idx]
            text_col = "black" if idx == 2 else "white"

            wrapped_ans = textwrap.fill(ans, width=45)

            btn = ctk.CTkButton(ans_frame, text=wrapped_ans, font=("Arial", 18, "bold"), text_color=text_col,
                                fg_color=bg_color, hover_color=hover_color, corner_radius=10,
                                command=lambda a=ans: self.check_answer(a, correct_ans))
            btn.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")

        def update_timer(current_time):
            if current_time > 0:
                self.timer_label.configure(text=f"⏱ {current_time}s")
                self.timer_event = self.after(1000, update_timer, current_time - 1)
            else:
                self.check_answer("Brak Czasu", correct_ans)

        self.timer_event = self.after(1000, update_timer, time_left - 1)

    def check_answer(self, choosen_ans, correct_ans):
        if self.timer_event:
            self.after_cancel(self.timer_event)
            self.timer_event = None

        self.api.check_answer(self.my_pin, choosen_ans, self.my_nick)
        self.clear_screen()

        if choosen_ans == correct_ans:
            wynik_label = ctk.CTkLabel(self, text="Brawo! Poprawna odpowiedź!", font=("Arial", 40, "bold"),
                                       text_color="#2ECC71")
            wynik_label.pack(pady=(150, 30))
        elif choosen_ans == "Brak Czasu":
            wynik_label = ctk.CTkLabel(self, text="Koniec czasu!", font=("Arial", 40, "bold"), text_color="#E67E22")
            wynik_label.pack(pady=(150, 30))
        else:
            wynik_label = ctk.CTkLabel(self, text="Niestety, źle!", font=("Arial", 40, "bold"), text_color="#E74C3C")
            wynik_label.pack(pady=(120, 20))

            correct_label = ctk.CTkLabel(self, text=f"Poprawna odpowiedź to:\n\n{correct_ans}",
                                         font=("Arial", 24, "bold"), text_color="white", wraplength=700)
            correct_label.pack(pady=20)

        response = self.api.check_room_status(self.my_pin)
        host_name = response.get("host")

        if self.my_nick == host_name:
            next_btn = ctk.CTkButton(self, text="Następna runda", font=("Arial", 28, "bold"), height=70, width=300,
                                     command=lambda: self.click_next_round(host_name))
            next_btn.pack(pady=60)
        else:
            wait_label = ctk.CTkLabel(self, text="Czekaj, aż Host włączy kolejną rundę...", font=("Arial", 20))
            wait_label.pack(pady=60)
            self.result_radar()

    def click_next_round(self, host_name):
        response = self.api.next_round(self.my_pin)
        if response and response.get("status") == "continue":
            self.loading_screen()
            self.update()

            def fetch_q():
                self.api.get_question(self.my_pin)

            threading.Thread(target=fetch_q).start()
            self.question_radar()
        elif response and response.get("status") == "results":
            self.result_radar()


    def results_screen(self, scores):
        self.clear_screen()
        title = ctk.CTkLabel(self, text="WYNIKI KOŃCOWE", font=("Arial", 50, "bold"), text_color="#F1C40F")
        title.pack(pady=(60, 40))

        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

        score_frame = ctk.CTkFrame(self, fg_color="#2C3E50", corner_radius=15)
        score_frame.pack(pady=10, padx=100, fill="x")

        for idx, (player, score) in enumerate(sorted_scores):
            prefix = "1" if idx == 0 else ("2" if idx == 1 else "3")
            score_label = ctk.CTkLabel(score_frame, text=f"{prefix} {player}: {score} pkt", font=("Arial", 32, "bold"))
            score_label.pack(pady=20)

        def back_to_menu():
            self.my_nick = ""
            self.my_pin = ""
            self.my_current_round = 0
            self.show_main_menu()

        back_btn = ctk.CTkButton(self, text="Wróć do Menu Głównego", font=("Arial", 24, "bold"), height=60, width=400,
                                 command=back_to_menu)
        back_btn.pack(pady=60)


if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()