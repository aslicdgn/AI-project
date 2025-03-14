from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from chatbots.chatbot import get_response, learn_new_response
from django.shortcuts import render

@csrf_exempt  # Eğer POST isteği gönderiliyorsa CSRF korumasını geçersiz kılar
def chatbot_response(request):

    if request.method == "GET":
        return render(request, "chatbot_app/chatbot.html")
    """
    Chatbot API endpoint.
    Kullanıcının mesajını alır, veritabanından uygun yanıtı döndürür ya da yeni bir yanıt öğrenmesini sağlar.
    """
    if request.method == 'POST':
        try:
            # JSON verisi almak
            data = json.loads(request.body)
            user_input = data.get('message', '').strip()

            if user_input:
                # Yanıtı al
                response = get_response(user_input)
                return JsonResponse({"response": response})
            else:
                return JsonResponse({"error": "Mesaj boş olamaz!"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Geçersiz JSON verisi!"}, status=400)
    
    return JsonResponse({"error": "Sadece POST istekleri kabul edilir!"}, status=405)

@csrf_exempt
def learn_new_input(request):
    """
    Kullanıcının yeni bir mesajı öğrenmesini sağlar.
    """
    if request.method == 'POST':
        try:
            # JSON verisi almak
            data = json.loads(request.body)
            user_input = data.get('message', '').strip()
            
            if user_input:
                # Yeni bir yanıt öğren
                learn_new_response(user_input)
                return JsonResponse({"message": f"Yeni yanıt '{user_input}' öğrenildi!"})
            else:
                return JsonResponse({"error": "Mesaj boş olamaz!"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Geçersiz JSON verisi!"}, status=400)
    
    return JsonResponse({"error": "Sadece POST istekleri kabul edilir!"}, status=405)
