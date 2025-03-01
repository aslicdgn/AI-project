def chatbot():
    greetings = ["merhaba", "selam", "hey", "nasılsın", "naber", "günaydın", "iyi akşamlar"]
    responses = {"merhaba": "Merhaba!", "selam": "Selam!", "hey": "Hey!", "nasılsın": "iyiyim, sen nasılsın?", "naber": "Biraz kötüyüm, sen nasılsın?", "günaydın": "Günaydın!", "iyi akşamlar": "İyi akşamlar!"}
    
    while True:
        user_input = input("Sen: ").lower()
        if user_input in greetings:
            print("Bot:", responses.get(user_input, "Merhaba!"))
        elif user_input == "çıkış":
            print("Bot: Görüşürüz!")
            break
        else:
            print("Bot: Sadece selamlaşma biliyorum! 'çıkış' yazarak çıkabilirsin.")

chatbot()
