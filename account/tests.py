from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

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
        self.assertEqual(user.username, self.user_date["username"])
        self.assertTrue(user.check_password(self.user_date["password"]))
        self.assertTrue(user.is_active)
        self.asserFalse(user.is_staff)
        self.asserFalse(user.is_superuser)

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
