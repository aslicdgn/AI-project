import sqlite3
import os
import random

DB_DIR = "db"
DB_PATH = os.path.join(DB_DIR, "chatbot.db")

def create_database():
    """Creates the database and ensures the 'db' directory exists."""
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Enable foreign keys if needed (but we are not using them in responses)
    cursor.execute("PRAGMA foreign_keys = ON")

    # Create greetings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS greetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT UNIQUE
        )
    """)

    # Create favorites table (optional – for future use)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT UNIQUE
        )
    """)

    # Create responses table using polymorphic association
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_table TEXT,
            source_id INTEGER,
            bot_response TEXT
        )
    """)

    conn.commit()
    conn.close()

def insert_greetings():
    """Inserts greeting data into the database if not already present."""
    greetings_data = {
        "merhaba": ["Merhaba!", "Selam!", "Hoş geldin!"],
        "selam": ["Selam!", "Merhaba!", "Hey!"],
        "hey": ["Hey!", "Selam!", "Naber?"],
        "nasılsın": ["İyiyim, sen nasılsın?", "Fena değil, ya sen?", "Harikayım!"],
        "günaydın": ["Günaydın!", "Hayırlı sabahlar!", "Günaydın, güzel bir gün olsun!"],
        "iyi akşamlar": ["İyi akşamlar!", "Akşamın güzel geçsin!", "İyi akşamlar, nasılsın?"],
        "iyi geceler": ["İyi geceler!", "Tatlı rüyalar!", "İyi uykular!"],
        "ne haber": ["İyilik, senden?", "Hadi anlat bakalım, ne var ne yok?", "Keyfim yerinde, sen nasılsın?"],
        "selamün aleyküm": ["Aleyküm selam!", "Ve aleyküm selam!", "Selam dostum!"],
        "alo": ["Alo! Buyur?", "Buradayım, seni dinliyorum!", "Evet, alo?"],
        "hoş geldin": ["Hoş bulduk!", "Teşekkürler, hoş buldum!", "Hoş bulduk, nasılsın?"],
        "görüşürüz": ["Görüşmek üzere!", "Sonra görüşürüz!", "Kendine iyi bak!"]
    }
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert greetings into the greetings table
    for user_input, responses in greetings_data.items():
        cursor.execute("INSERT OR IGNORE INTO greetings (user_input) VALUES (?)", (user_input,))
    
    # For each greeting, insert its responses into the responses table.
    # The responses table uses a polymorphic association:
    #   - source_table: "greetings"
    #   - source_id: the id of the greeting in the greetings table.
    for user_input, responses in greetings_data.items():
        cursor.execute("SELECT id FROM greetings WHERE user_input = ?", (user_input,))
        source_id = cursor.fetchone()[0]
        for response in responses:
            cursor.execute(
                "INSERT OR IGNORE INTO responses (source_table, source_id, bot_response) VALUES (?, ?, ?)",
                ("greetings", source_id, response)
            )
    
    conn.commit()
    conn.close()

def create_new_table(table_name):
    """Creates a new category table for dynamic topics."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT UNIQUE
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"Yeni kategori oluşturuldu: {table_name}")

def learn_new_response(user_input):
    """
    Learns a new response for an unknown input.
    It asks which category to store the new response in, creates that table if needed,
    then inserts the input into that category table and also (if desired) into greetings.
    Finally, it stores the response in the responses table using a polymorphic association.
    """
    print("Bot: Bunu bilmiyorum. Hangi kategoride saklamalıyım? (Örn: greetings, favorites, yemek, spor, tarih)")
    category = input("Sen: ").strip().lower()

    # For standard categories (greetings, favorites) assume they exist.
    # For any other category, create the table.
    if category not in ("greetings", "favorites"):
        create_new_table(category)

    print(f"Bot: '{user_input}' için nasıl cevap vermeliyim?")
    new_response = input("Sen: ").strip()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert into the selected category table (or update standard ones)
    cursor.execute(f"INSERT OR IGNORE INTO {category} (user_input) VALUES (?)", (user_input,))
    cursor.execute(f"SELECT id FROM {category} WHERE user_input = ?", (user_input,))
    source_id = cursor.fetchone()[0]

    # Optionally, ensure the input is also in greetings if the category is not greetings
    if category != "greetings":
        cursor.execute("INSERT OR IGNORE INTO greetings (user_input) VALUES (?)", (user_input,))

    # Insert the new response into responses using polymorphic association.
    cursor.execute(
        "INSERT INTO responses (source_table, source_id, bot_response) VALUES (?, ?, ?)",
        (category, source_id, new_response)
    )

    conn.commit()
    conn.close()
    print(f"Bot: Artık '{user_input}' dediğinde '{new_response}' yanıtını vereceğim ({category} kategorisinde).")

def get_response(user_input):
    """Retrieves a response from the database based on user input."""
    user_input = user_input.strip().lower()
    responses_found = []
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get list of all user-defined tables (exclude responses and sqlite_sequence)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT IN ('responses', 'sqlite_sequence')")
    tables = [row[0] for row in cursor.fetchall()]

    for table in tables:
        try:
            # For each table, check if there's a matching user_input.
            query = f"SELECT id FROM {table} WHERE user_input = ?"
            cursor.execute(query, (user_input,))
            result = cursor.fetchone()
            if result:
                source_id = result[0]
                # Retrieve all responses associated with this entry.
                cursor.execute(
                    "SELECT bot_response FROM responses WHERE source_table = ? AND source_id = ?",
                    (table, source_id)
                )
                responses_found.extend([row[0] for row in cursor.fetchall()])
        except sqlite3.Error as e:
            # If a table doesn't have the expected structure, skip it.
            print(f"Error querying table {table}: {e}")
            continue

    conn.close()

    if responses_found:
        return random.choice(responses_found)
    else:
        learn_new_response(user_input)
        return "Tamam, öğrendim!"

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

if __name__ == "__main__":
    chatbot()