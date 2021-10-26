from django.test import TestCase
from django.test.client import Client
from django.conf import settings

from users.models import NormalUser

# Create your tests here.

class TestMainSmokeUsers(TestCase):
	success_code = 200
	redirect_code = 302
	username = "user_name_1"
	email = "someemail@mail.ru"
	password = "Q1wertyu"

	new_user_data = {
		"username": "user_name_2",
		"first_name": "first_name_2",
		"last_name": "last_name_2",
		"email": "anotheremail@mail.ru",
		"password1": "Q1wertyu",
		"password2": "Q1wertyu",

	}

	def setUp(self) -> None:
		self.user = NormalUser.objects.create_superuser(self.username, email=self.email, password=self.password)
		self.client = Client()

	def test_login(self):
		response = self.client.get("/")
		self.assertEqual(response.status_code, self.success_code)
		self.assertTrue(response.context["user"].is_anonymous)

		self.client.login(username=self.username, password=self.password)

		response = self.client.get("/users/login/")
		self.assertEqual(response.status_code, self.redirect_code)

	def test_register(self):
		response = self.client.post("/users/register/", data=self.new_user_data)
		self.assertEqual(response.status_code, self.redirect_code)

		new_user = NormalUser.objects.get(username=self.new_user_data["username"])
		activation_url = f"{settings.DOMAIN_NAME}/users/verify/{self.new_user_data['email']}/{new_user.activation_key}/"
		response = self.client.get(activation_url)
		self.assertEqual(response.status_code, self.success_code)

	def tearDown(self) -> None:
		pass