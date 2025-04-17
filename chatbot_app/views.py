from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import subprocess
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


@csrf_exempt
def chatbot_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_input = data.get("message", "")

        if not user_input:
            return JsonResponse({"error": "Boş mesaj gönderildi."}, status=400)

        # subprocess ile chatbot.py'yi input ile çalıştır
        try:
            process = subprocess.Popen(
                ["python", "chatbot.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # chatbot.py birkaç input() bekliyor olabilir, bu nedenle gerekirse ek input ekleyebiliriz
            output, error = process.communicate(input=user_input + "\n")  # ilk input kullanıcı mesajı

            if error:
                return JsonResponse({"error": error}, status=500)

            # Son satırı al, genellikle bot cevabı
            response_lines = output.strip().split("\n")
            bot_response = response_lines[-1] if response_lines else "Bir hata oluştu."

            return JsonResponse({"response": bot_response})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)