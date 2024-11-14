from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.http import JsonResponse
from .forms import CustomLoginForm

def custom_login_view(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Здесь перенаправляем на представление для проверки группы
            return JsonResponse({"success": True, "redirect_url": "/redirect/"})  # Замените "/redirect/" на URL нужного представления

        # Возвращаем JSON с ошибкой, если данные неверны
        return JsonResponse({"success": False, "error": "Неправильно введен логин или пароль. Проверьте правильность"})

    # При GET-запросе возвращаем стандартный шаблон
    form = CustomLoginForm()
    return render(request, "login/sing_up.html", {"form": form})


@login_required
def redirect_user_based_on_group(request):
    user = request.user

    # Перенаправляем в зависимости от группы пользователя
    if user.groups.filter(name="Администратор").exists():
        return redirect("panel_admin")
    elif user.groups.filter(name="Инженер").exists():
        return redirect("engineer_dashboard")  # Замените на нужный URL-адрес
    elif user.groups.filter(name="Бухгалтер").exists():
        return redirect("accountant_dashboard")  # Замените на нужный URL-адрес
    elif user.groups.filter(name="Менеджер").exists():
        return redirect("manager_dashboard")  # Замените на нужный URL-адрес
    elif user.groups.filter(name="Руководитель").exists():
        return redirect("leader_dashboard")  # Замените на нужный URL-адрес
    else:
        return redirect("default_dashboard")  # Замените на нужный URL-адрес для всех остальных



def is_admin(user):
    return user.is_authenticated and user.groups.filter(name="Администратор").exists()


@user_passes_test(is_admin, login_url='access_denied')
def panel_admin(request):
    context= {
            'username' : request.user.username,
        }
    return render(request, "panel/admin_panel.html", context)


def access_denied(request):
    return render(request, "errors/403.html")