import sqlite3
import os
import random

# Define database path inside the "db" directory
DB_DIR = "db"
DB_PATH = os.path.join(DB_DIR, "chatbot.db")

def create_database():
    """Creates the database and ensures the 'db' directory exists."""
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)  # Create "db" folder if it doesn't exist
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS greetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT UNIQUE,
            bot_response TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_greetings():
    """Inserts greeting data into the database if not already present."""
    greetings_data = [
        ("merhaba", ["Merhaba!", "Selam!", "Hoş geldin!"]),
        ("selam", ["Selam!", "Merhaba!", "Hey!"]),
        ("hey", ["Hey!", "Selam!", "Naber?"]),
        ("nasılsın", ["İyiyim, sen nasılsın?", "Fena değil, ya sen?", "Harikayım!"]),
        ("günaydın", ["Günaydın!", "Hayırlı sabahlar!", "Günaydın, güzel bir gün olsun!"]),
        ("iyi akşamlar", ["İyi akşamlar!", "Akşamın güzel geçsin!", "İyi akşamlar, nasılsın?"]),
        ("iyi geceler", ["İyi geceler!", "Tatlı rüyalar!", "İyi uykular!"]),
        ("ne haber", ["İyilik, senden?", "Hadi anlat bakalım, ne var ne yok?", "Keyfim yerinde, sen nasılsın?"]),
        ("selamün aleyküm", ["Aleyküm selam!", "Ve aleyküm selam!", "Selam dostum!"]),
        ("alo", ["Alo! Buyur?", "Buradayım, seni dinliyorum!", "Evet, alo?"]),
        ("hoş geldin", ["Hoş bulduk!", "Teşekkürler, hoş buldum!", "Hoş bulduk, nasılsın?"]),
        ("görüşürüz", ["Görüşmek üzere!", "Sonra görüşürüz!", "Kendine iyi bak!"])
    ]
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for user_input, responses in greetings_data:
        for response in responses:
            cursor.execute("INSERT OR IGNORE INTO greetings (user_input, bot_response) VALUES (?, ?)", (user_input, response))
    
    conn.commit()
    conn.close()

def get_response(user_input):
    """Retrieves a response from the database based on user input."""
    user_input = user_input.strip().lower()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT bot_response FROM greetings WHERE user_input = ?", (user_input,))
    responses = cursor.fetchall()
    
    conn.close()
    
    if responses:
        return random.choice([response[0] for response in responses])
    
    # Alternative responses for unknown inputs
    unknown_responses = [
        "Bunu bilmiyorum ama öğrenebilirim!",
        "Şu an sadece selamlaşmaları biliyorum ama yakında daha fazlasını öğreneceğim!",
        "Bunu anlayamadım ama yakında daha akıllı olacağım!",
        "Şimdilik sadece selamlaşmalar konusunda iyiyim. Başka bir şey deneyelim mi?"
    ]
    
    return random.choice(unknown_responses)

def chatbot():
    """Runs the chatbot loop."""
    create_database()
    insert_greetings()
    
    print("Bot: Merhaba! Selamlaşabilirim. 'çıkış' yazarak sohbeti bitirebilirsin.")
    
    while True:
        user_input = input("Sen: ").strip()
        if user_input.lower() == "çıkış":
            print("Bot: Görüşürüz! Kendine iyi bak. 👋")
            break
        print("Bot:", get_response(user_input))

chatbot()
