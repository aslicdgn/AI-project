def chatbot():
    greetings = ["merhaba", "selam", "hey", "nasılsın", "günaydın", "iyi akşamlar", "iyi geceler", "ne haber", "selamün aleyküm", "alo", "hoş geldin", "görüşürüz"]
    responses = {
        "merhaba": "Merhaba!", "selam": "Selam!", "hey": "Hey!", "nasılsın": "İyiyim, sen nasılsın?",
        "günaydın": "Günaydın!", "iyi akşamlar": "İyi akşamlar!", "iyi geceler": "İyi geceler! Tatlı rüyalar!",
        "ne haber": "İyilik, senden?", "selamün aleyküm": "Aleyküm selam!", "alo": "Alo! Buyur?",
        "hoş geldin": "Hoş bulduk!", "görüşürüz": "Görüşmek üzere!"
    }
    
    while True:
        user_input = input("Sen: ").lower()
        if user_input in greetings:
            print("Bot:", responses.get(user_input, "Merhaba!"))
        elif user_input == "ben gidiyorum":
            print("Bot: Görüşürüz!")
            break
        else:
            print("Bot: Sadece selamlaşma biliyorum! 'ben gidiyorum' yazarak çıkabilirsin.")

chatbot()

