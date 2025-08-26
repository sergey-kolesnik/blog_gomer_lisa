from django.urls import path
from .views import IndexPageView,  LoginView, RegisterView

app_name = 'account'

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('login/', LoginView, name='login'),
    path('register/', RegisterView, name='register'),
]
