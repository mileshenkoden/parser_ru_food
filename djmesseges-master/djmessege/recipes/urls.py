from venv import create
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.recipes_home, name='recipes_home'),
    path('create', views.create, name='create'),
    path('<int:pk>/update', views.NewUpdateView.as_view(), name='recipes-update'),
    path('<int:pk>', views.NewDetailView.as_view(), name='recipes-detail'),
    path('<int:pk>/delete', views.NewDeleteView.as_view(), name='recipes-delete'),

]

