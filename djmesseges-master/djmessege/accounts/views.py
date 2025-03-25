from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django import forms
from django.contrib import messages
from .forms import CustomUserCreationForm
from .forms import UsernameAuthenticationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Реєстрація успішна! Тепер увійдіть.')
            return redirect('login')  # Перенаправляємо на сторінку входу
        else:
            error_messages = [f"{field}: {' '.join(errors)}" for field, errors in form.errors.items()]
            messages.error(request, f"Помилка реєстрації: {'; '.join(error_messages)}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UsernameAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Успішний вхід!')
                return redirect('home')  # замініть на вашу домашню сторінку
            else:
                messages.error(request, 'Неправильний username або пароль.')
        else:
            messages.error(request, 'Будь ласка, виправте помилки.')
    else:
        form = UsernameAuthenticationForm()  # тут нічого не передається в form без POST

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Ви успішно вийшли із системи.')
    return redirect('login')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')
