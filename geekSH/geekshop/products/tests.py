from django.test import TestCase
from django.test.client import Client

from products.models import ProductCategory, Product

# Create your tests here.

class TestMainSmokeProducts(TestCase):
	success_code = 200
	redirect_code = 302

	def setUp(self) -> None:
		category = ProductCategory.objects.create(name="Test_Category")
		Product.objects.create(category=category, name="Test_Product", price=500)

		self.client = Client()

	def test_products_pages(self):
		response = self.client.get("/")
		self.assertEqual(response.status_code, self.success_code)

	def test_product_detail(self):
		for product_item in Product.objects.all():
			response = self.client.get(f"/products/detail_product/{product_item.pk}")
			self.assertEqual(response.status_code, self.success_code)

	def test_profile_basket(self):
		response = self.client.get("/users/profile/")
		self.assertEqual(response.status_code, self.redirect_code)

	def tearDown(self) -> None:
		pass