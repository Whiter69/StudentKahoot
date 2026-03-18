import customtkinter as ctk
import api_siec

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.geometry("800x600")
app.title("Quiz-Klient")

def click_dolacz_do_gry():
    player=nick_entry.get()
    pin=pin_entry.get()
    if player=="" or pin=="":
        making_game_info.configure(text="Podaj swoją nazwę i PIN!", text_color="red")
        return
    making_game_info.configure(text="Łączenie z serwerem...",text_color="green")
    app.update()
    sukces,message=api_siec.join_room(pin,player)
    if sukces:
        making_game_info.configure(text=message,text_color="green")
    else:
        making_game_info.configure(text=message,text_color="red")

def click_stworz_gre():
    player=nick_entry.get()

    if player=="":
        making_game_info.configure(text="Podaj swoją nazwę!", text_color="red")
        return

    making_game_info.configure(text="Łączenie z serwerem...", text_color="green")

    app.update()
    generated_pin = api_siec.make_new_room()

    making_game_info.configure(text=f"Twój PIN do gry to: {generated_pin}", text_color="green")

app.grid_columnconfigure(0, weight=20)

title = ctk.CTkLabel(app, text="Witaj w Quizie!", font=("Arial", 44, "bold"))
title.grid(row=0, column=0, pady=(40, 0), padx=10)

nick_entry=ctk.CTkEntry(app,placeholder_text= "Twoja nazwa",width=200, height=30,font=("Arial", 16))
nick_entry.grid(row=1, column=0, pady=(20, 10), padx=20)

button_stworz = ctk.CTkButton(app, text="Stwórz nowy pokój", command=click_stworz_gre, height=40)
button_stworz.grid(row=2, column=0, pady=20)

pin_entry=ctk.CTkEntry(app,placeholder_text= "PIN do gry",width=200, height=30,font=("Arial", 16))
pin_entry.grid(row=3, column=0, pady=(20, 10), padx=20)

button_dolacz = ctk.CTkButton(app, text="Dołącz do gry", command=click_dolacz_do_gry, height=40)
button_dolacz.grid(row=4, column=0, pady=20)

making_game_info = ctk.CTkLabel(app, text="", font=("Arial", 18))
making_game_info.grid(row=5, column=0, pady=20, padx=20)


if __name__ == "__main__":
    app.mainloop()