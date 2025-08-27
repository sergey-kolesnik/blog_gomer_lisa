from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.views.generic import TemplateView


from .forms import CustomUserCreationForm

class ModelTests(TestCase):
    """Тесты для модели пользователя"""

    def setUp(self):
        """Подготовка данных для теста"""
        self.User = get_user_model()
        self.user_data = {
            "email": "test@example.com",
            "username": "test_user",
            "password": "testpass123",
        }

    def test_create_user_successful(self):
        """Тест: успешное создание пользователя"""
        user = self.User.objects.create_user(**self.user_data)

        self.assertEqual(user.email, self.user_data["email"])
        self.assertEqual(user.username, self.user_data["username"])
        self.assertTrue(user.check_password(self.user_data["password"]))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_with_email_raises_error(self):
        """Тест: создание поользователя без email вызывает ошибку"""
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email=None,
                username=self.user_data["username"],
                password=self.user_data["password"]
            )

    def test_create_superuser_successful(self):
        """Тест: успешное создание суперпользователя"""
        admin_user = self.User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="adminpass123"
        )

        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_user_string_representation(self):
        """Тест: строковое представление пользователя"""
        user = self.User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data["username"])

class IndexPageTests(TestCase):
    """Тесты для главной страницы"""
    def test_index_page_url_exists(self):
        """Тест: главная страница доступна по url"""
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)

    def test_index_page_uses_corretc_templates(self):
        """Тест: используется правильный шаблон"""
        response = self.client.get(reverse("account:index"))
        # self.assertContains(response, '<a href="{% url 'account:login' %}" class="account-page__link">Sign up</a>', html=True)
        # self.assertContains(response, '<a href="/register/">Register</a>', html=True)

    def test_index_view_uses_template_view(self):
        """Тест: view использует TemplateView"""
        from account.views import IndexPageView
        self.assertTrue(issubclass(IndexPageView, TemplateView))



class RegistrationViewTests(TestCase):
    """Тест для view-функции регистрации"""
    def test_get_request_shows_form(self):
        """Тест: GET-запрос отображает форму регистрации"""
        response = self.client.get(reverse("account:register"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_registration_form_displayed(self):
        """Тест: правильно отображается форма"""
        responce = self.client.get(reverse("account:register"))
        self.assertContains(responce, "form")
        self.assertContains(responce, "email")
        self.assertContains(responce, "username")
        self.assertContains(responce, "password")


    def test_post_request_creates_new_user(self):
        """Тест: POST-запрос регистрирует нового пользователя"""
        data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        }
        response = self.client.post(reverse("account:register"), data)
        self.assertEqual(response.status_code, 302)
        User = get_user_model()
        self.assertTrue(User.objects.filter(email='testuser@example.com').exists())


    def test_post_request_with_invalid_data(self):
        """Тест: POST-запрос с некорректными данными"""
        invalid_data = {
            'email': 'invalid-email',
            'username': '',
            'password1': 'short',
            'password2': 'short',
        }
        response = self.client.post(reverse("account:register"), invalid_data)
        self.assertEqual(response.status_code, 200)  # Ошибочная форма остаётся на той же странице
        self.assertContains(response, 'error')
        User = get_user_model()
        self.assertFalse(User.objects.filter(email='invalid-email').exists())