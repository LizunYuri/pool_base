from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views  import LoginView
from .forms import CustomLoginForm
from django.http import JsonResponse


def custom_login_view(request):
    if request.method == "POST" and request.is_ajax():
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return JsonResponse({"success": True, "redirect_url": "/"})  # Укажите нужный URL для перенаправления

        # Возвращаем JSON с ошибкой, если данные неверны
        return JsonResponse({"success": False, "error": "Invalid username or password."})

    # При GET-запросе возвращаем стандартный шаблон
    form = CustomLoginForm()
    return render(request, "login/sing_up.html", {"form": form})
    