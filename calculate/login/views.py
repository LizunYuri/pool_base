from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, update_session_auth_hash
from django.http import JsonResponse
from .forms import CustomLoginForm, UserUpdateForm, UserPasswordChangeForm
from .models import Company

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

def is_supervisor(user):
    return user.is_authenticated and user.groups.filter(name="Руководитель").exists()

def is_engineer(user):
    return user.is_authenticated and user.groups.filter(name="Инженер").exists()

def is_manager(user):
    return user.is_authenticated and user.groups.filter(name="Менеджер").exists()

def is_accountant(user):
    return user.is_authenticated and user.groups.filter(name="Бухгалтер").exists()


@login_required
def user_profile(request):
    user = request.user

    companies = Company.objects.filter(personal=user)

    return render(request, 'login/user_profile.html', {'user' : user})




@login_required
def update_form(request):
    user = request.user
    user_form = UserUpdateForm(instance=user)
    password_form = UserPasswordChangeForm(user)
    return render(request, 'login/update_profile.html', {
        'user_form': user_form,
        'password_form': password_form,
    })


@login_required
def profile_update(request):

    print("POST request received:", request.POST)  # Логируем данные POST запроса

    if request.method == 'POST':
        # Обработка данных профиля
        if 'update_profile' in request.POST:
            print("Обрабатываем форму профиля")  # Логируем начало обработки
            user_form = UserUpdateForm(request.POST, instance=request.user)

            # Проверка валидности формы
            if user_form.is_valid():
                user_form.save()
                return JsonResponse({'success': True, 'message': 'Данные профиля обновлены.'})
            else:
                print("Ошибки формы:", user_form.errors)  # Логируем ошибки
                return JsonResponse({'success': False, 'errors': user_form.errors})

       # Обработка смены пароля
        elif 'change_password' in request.POST:
            print("Обрабатываем форму смены пароля")  # Логируем начало обработки
            password_form = UserPasswordChangeForm(request.user, request.POST)

            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, request.user)  # Обновляем сессию после смены пароля
                return JsonResponse({'success': True, 'message': 'Пароль успешно изменён.'})
            else:
                
                print("Ошибки формы пароля:", password_form.errors)  # Логируем ошибки
                return JsonResponse({'success': False, 'errors': password_form.errors})

    return JsonResponse({'success': False, 'message': 'Неверный запрос.'})





@user_passes_test(is_admin, login_url='access_denied')
def panel_admin(request):
    context= {
            'username' : request.user.username,
        }
    return render(request, "panel/admin_panel.html", context)


def access_denied(request):
    return render(request, "errors/403.html")