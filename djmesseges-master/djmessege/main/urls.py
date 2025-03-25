from django.urls import path, include  # Імпортуємо include
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # Головна сторінка
    path('about/', views.about, name='about'),  # Сторінка "Про нас"
    path('accounts/', include('accounts.urls')),  # Включення маршрутів з accounts
]
