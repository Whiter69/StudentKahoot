import sqlite3


def stworz_baze():
    conn = sqlite3.connect("quiz_baza.db")
    cursor = conn.cursor()

    print("Tworzenie tabel w bazie...")

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS pytania
                   (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                       kategoria TEXT,
                       tresc TEXT,
                       odp_a TEXT, odp_b TEXT, odp_c TEXT, odp_d TEXT,
                       poprawna TEXT
                   )
                   ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS mecze
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       pin TEXT,
                       kategoria TEXT,
                       data_gry TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )
                   ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS wyniki
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       mecz_id INTEGER,
                       gracz TEXT,
                       punkty INTEGER, 
                       FOREIGN KEY
                   (
                       mecz_id
                   ) REFERENCES mecze
                   (
                       id
                   )
                       )
                   ''')

    cursor.execute('DELETE FROM pytania')

    baza_pytan = {
        "Podstawy Programowania": [
            ("Co robi instrukcja 'print' w Pythonie?",
             ["Zamyka program", "Wyświetla tekst na ekranie", "Pobiera dane", "Usuwa plik"],
             "Wyświetla tekst na ekranie"),
            ("Jakiego symbolu używa się do tworzenia komentarzy w Pythonie?", ["//", "", "#", "/* */"], "#"),
            ("Który typ zmiennej przechowuje liczby całkowite?", ["String", "Float", "Boolean", "Integer"], "Integer"),
            ("Co oznacza skrót IDE?",
             ["Integrated Development Environment", "Internet Data Explorer", "Internal Design Engine",
              "Input Emulator"], "Integrated Development Environment"),
            ("Jak nazywa się pętla na określoną liczbę razy?", ["while", "do-while", "for", "if-else"], "for"),
            ("Co robi operator '%' (modulo)?", ["Oblicza procent", "Zwraca resztę z dzielenia", "Mnoży", "Zaokrągla"],
             "Zwraca resztę z dzielenia"),
            ("Struktura LIFO (Ostatnie weszło, pierwsze wyszło) to:", ["Kolejka", "Tablica", "Stos (Stack)", "Lista"],
             "Stos (Stack)"),
            ("Czym jest zmienna?", ["Nazwanym miejscem w pamięci", "Instrukcją warunkową", "Funkcją systemu", "Błędem"],
             "Nazwanym miejscem w pamięci"),
            ("Błąd dający zły wynik, ale nie przerywający programu to:",
             ["Syntax Error", "Runtime Error", "Błąd logiczny", "Błąd kompilacji"], "Błąd logiczny"),
            ("Do czego służy 'if'?",
             ["Do pętli", "Do zmiennych", "Do wykonywania kodu po spełnieniu warunku", "Do importu"],
             "Do wykonywania kodu po spełnieniu warunku")
        ],
        "Bazy danych": [
            ("Co oznacza SQL?",
             ["Structured Query Language", "Simple Question Language", "System Quality Layout", "Server Query"],
             "Structured Query Language"),
            ("Polecenie do pobierania danych?", ["UPDATE", "SELECT", "INSERT", "DELETE"], "SELECT"),
            ("Klucz główny (Primary Key) to:",
             ["Hasło", "Unikalny identyfikator rekordu", "Główny serwer", "Szyfrowanie"],
             "Unikalny identyfikator rekordu"),
            ("Polecenie do modyfikacji istniejących danych?", ["UPDATE", "ALTER", "MODIFY", "CHANGE"], "UPDATE"),
            ("Łączenie danych z dwóch tabel to:", ["COMBINE", "MERGE", "JOIN", "LINK"], "JOIN"),
            ("Klauzula do filtrowania wyników to:", ["WHERE", "FILTER", "ORDER BY", "GROUP BY"], "WHERE"),
            ("Akronim ACID to:", ["Atomicity, Consistency, Isolation, Durability", "Active, Control, Input, Data",
                                  "Auto, Create, Insert, Delete", "Access"],
             "Atomicity, Consistency, Isolation, Durability"),
            ("Czym jest indeks w bazie?",
             ["Spisem treści", "Kopią", "Strukturą przyspieszającą wyszukiwanie", "Hasłem"],
             "Strukturą przyspieszającą wyszukiwanie"),
            ("Wstawienie nowego rekordu?", ["ADD RECORD", "INSERT INTO", "CREATE DATA", "NEW ROW"], "INSERT INTO"),
            ("Co oznacza NoSQL?", ["No Server Query", "Not Only SQL", "No Standard Query", "Non-Sequential"],
             "Not Only SQL")
        ],
        "Sztuczna Inteligencja": [
            ("Czym jest 'Machine Learning'?", ["Robotyka", "Uczenie maszynowe", "Naprawa procesorów", "Sieć neuronowa"],
             "Uczenie maszynowe"),
            ("Test inteligencji maszyny?", ["Turinga", "Newtona", "Einsteina", "Muska"], "Turinga"),
            ("Poddziedzina inspirowana mózgiem?",
             ["Drzewa decyzyjne", "Algorytmy genetyczne", "Sieci neuronowe", "Logika rozmyta"], "Sieci neuronowe"),
            ("Do czego służy NLP?", ["Grafika 3D", "Analiza języka naturalnego", "Sterowanie dronami", "Matematyka"],
             "Analiza języka naturalnego"),
            ("Uczenie z systemem kar i nagród?",
             ["Nadzorowane", "Nienadzorowane", "Ze wzmocnieniem (Reinforcement)", "Głębokie"],
             "Ze wzmocnieniem (Reinforcement)"),
            ("Overfitting to:",
             ["Zbyt wolne uczenie", "Zbyt mocne dopasowanie do danych treningowych", "Przegrzewanie", "Brak danych"],
             "Zbyt mocne dopasowanie do danych treningowych"),
            ("Architektura ChatGPT to:", ["CNN", "GAN", "Transformer", "SVM"], "Transformer"),
            ("Halucynacje AI to:",
             ["Błąd graficzny", "Generowanie fałszywych informacji z przekonaniem", "Uszkodzenie dysku", "Odmowa"],
             "Generowanie fałszywych informacji z przekonaniem"),
            ("Skrót LLM?", ["Low Machine", "Logic Method", "Large Language Model", "Local Module"],
             "Large Language Model"),
            ("Dostosowywanie modelu do zadania to:", ["Formatowanie", "Fine-tuning", "Overclocking", "Debugging"],
             "Fine-tuning")
        ],
        "Cyberbezpieczeństwo": [
            ("Phishing to:", ["Ochrona", "Kradzież danych przez podszywanie się", "Szyfrowanie", "Odzyskiwanie"],
             "Kradzież danych przez podszywanie się"),
            ("Atak DDoS polega na:",
             ["Przejęciu kamery", "Zalaniu serwera zapytaniami", "Kradzieży haseł", "Zniszczeniu kabli"],
             "Zalaniu serwera zapytaniami"),
            ("Protokół szyfrowanego WWW to:", ["HTTP", "FTP", "HTTPS", "Telnet"], "HTTPS"),
            ("Skrót VPN?", ["Virtual Private Network", "Virus Protection Node", "Visual Navigator", "Verified Name"],
             "Virtual Private Network"),
            ("Ransomware to:", ["Optymalizator", "Wirus szyfrujący pliki dla okupu", "Antywirus", "Pulpit zdalny"],
             "Wirus szyfrujący pliki dla okupu"),
            ("Brute Force to:",
             ["Sprawdzanie wszystkich kombinacji haseł", "AI antywirus", "Firewall", "Klucz asymetryczny"],
             "Sprawdzanie wszystkich kombinacji haseł"),
            ("Zasada 'Least Privilege'?",
             ["Darmowe oprogramowanie", "Tylko niezbędne uprawnienia do pracy", "Brak praw", "Pełny dostęp"],
             "Tylko niezbędne uprawnienia do pracy"),
            ("Uwierzytelnianie MFA to:",
             ["Kilka kont", "Min. dwie formy weryfikacji tożsamości", "Ochrona serwerowni", "Długie hasło"],
             "Min. dwie formy weryfikacji tożsamości"),
            ("Exploit to:", ["Osoba", "Antywirus", "Kod wykorzystujący lukę w systemie", "Odzyskiwanie"],
             "Kod wykorzystujący lukę w systemie"),
            ("White Hat Hacker to:",
             ["Twórca wirusów", "Etyczny haker testujący zabezpieczenia", "Przestępca", "Helpdesk"],
             "Etyczny haker testujący zabezpieczenia")
        ]
    }

    print("Wgrywanie pytań...")
    for kategoria, pytania in baza_pytan.items():
        for pytanie in pytania:
            tresc = pytanie[0]
            odp = pytanie[1]
            poprawna = pytanie[2]
            cursor.execute('''
                           INSERT INTO pytania (kategoria, tresc, odp_a, odp_b, odp_c, odp_d, poprawna)
                           VALUES (?, ?, ?, ?, ?, ?, ?)
                           ''', (kategoria, tresc, odp[0], odp[1], odp[2], odp[3], poprawna))

    conn.commit()
    conn.close()
    print("GOTOWE! Plik 'quiz_baza.db' został utworzony.")


if __name__ == "__main__":
    stworz_baze()