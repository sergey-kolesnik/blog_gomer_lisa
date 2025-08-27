
from django.urls import path
from .views import BlogIndexView

app_name = 'blog'

urlpatterns = [
    path('', BlogIndexView, name='index'),  # Главная страница блога
]