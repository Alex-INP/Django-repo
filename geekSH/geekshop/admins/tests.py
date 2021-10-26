from django.test import TestCase
from django.test.client import Client
from django.conf import settings

from users.models import NormalUser
from products.models import ProductCategory, Product
# Create your tests here.

class TestMainSmokeAdmins(TestCase):
	success_code = 200
	redirect_code = 302
	username = "user_name_1"
	email = "someemail@mail.ru"
	password = "Q1wertyu"

	category_data ={
		"name": "new_name",
		"description": "new_description",
	}
	category_data_2 = {
		"name": "new_cat",
		"description": "cat_description",
	}



	def setUp(self) -> None:
		category = ProductCategory.objects.create(name="Test_Category", description="somedesc")
		Product.objects.create(category=category, name="Test_Product", price=500)
		self.user = NormalUser.objects.create_superuser(self.username, email=self.email, password=self.password)
		self.client = Client()

		self.product_data = {
			"name": "new_prod_name",
			"price": 250,
			"category": category.pk,
			"quantity": 20
		}
		self.product_data_2 = {
			"name": "new_prod",
			"price": 800,
			"category": category.pk,
			"quantity": 10
		}

	# -----------------------------------------Admin_category_tests-----------------------------------------

	def test_admin_index(self):
		self.client.login(username=self.username, password=self.password)
		response = self.client.get("/admins/")
		self.assertEqual(response.status_code, self.success_code)

	def test_admin_categories(self):
		self.client.login(username=self.username, password=self.password)
		response = self.client.get("/admins/category_show/")
		self.assertEqual(response.status_code, self.success_code)


	def test_admin_update_category(self):
		self.client.login(username=self.username, password=self.password)
		for category in ProductCategory.objects.all():
			response = self.client.get(f"/admins/category_update/{category.pk}")
			self.assertEqual(response.status_code, self.success_code)

			response = self.client.post(f"/admins/category_update/{category.pk}", data=self.category_data)
			self.assertEqual(response.status_code, self.redirect_code)

	def test_admin_create_category(self):
		self.client.login(username=self.username, password=self.password)
		response = self.client.post("/admins/category_create/", data=self.category_data_2)
		self.assertEqual(response.status_code, self.redirect_code)

	def test_admin_delete_category(self):
		self.client.login(username=self.username, password=self.password)
		for category in ProductCategory.objects.all():
			response = self.client.post(f"/admins/category_delete/{category.pk}")
			self.assertEqual(response.status_code, self.redirect_code)

#-----------------------------------------Admin_products_tests-----------------------------------------

	def test_admin_products(self):
		self.client.login(username=self.username, password=self.password)
		response = self.client.get("/admins/product_show/")
		self.assertEqual(response.status_code, self.success_code)


	def test_admin_update_product(self):
		self.client.login(username=self.username, password=self.password)
		for product in Product.objects.all():
			response = self.client.get(f"/admins/product_update/{product.pk}")
			self.assertEqual(response.status_code, self.success_code)

			response = self.client.post(f"/admins/product_update/{product.pk}", data=self.product_data)
			self.assertEqual(response.status_code, self.redirect_code)

	def test_admin_create_product(self):
		self.client.login(username=self.username, password=self.password)
		response = self.client.post("/admins/product_create/", data=self.product_data_2)
		self.assertEqual(response.status_code, self.redirect_code)

	def test_admin_delete_product(self):
		self.client.login(username=self.username, password=self.password)
		for product in ProductCategory.objects.all():
			response = self.client.post(f"/admins/product_delete/{product.pk}")
			self.assertEqual(response.status_code, self.redirect_code)

	def tearDown(self) -> None:
		pass