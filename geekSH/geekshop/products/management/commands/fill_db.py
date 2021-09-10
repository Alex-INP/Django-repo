from django.core.management.base import BaseCommand

from products.models import ProductCategory, Product
import os.path as path
import json


def get_data(target_file):
	with open(path.join("products/fixtures", target_file), "r", encoding="utf-8") as file:
		return json.load(file)

class Command(BaseCommand):
	def handle(self, *args, **options):
		product_categories = get_data("category.json")
		products = get_data("data.json")

		ProductCategory.objects.all().delete()
		for category in product_categories:
			cat = category['fields']
			new_category = ProductCategory(**cat)
			new_category.save()

		Product.objects.all().delete()
		for product in products:
			def_category = ProductCategory.objects.get(name="Одежда")
			product["category"] = def_category

			new_product = Product(**product)
			new_product.save()

