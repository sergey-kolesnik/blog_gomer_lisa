from django.urls import path
from .views import IndexPageView,  LoginView, RegisterView

app_name = 'account'

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView, name='login'),

]
