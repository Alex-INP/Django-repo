from django.db import models

from users.models import NormalUser
from products.models import Product
# Create your models here.

class Basket(models.Model):
	user = models.ForeignKey(NormalUser, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=0)
	created_at = models.TimeField(auto_now_add=True)
	updated_at = models.TimeField(auto_now=True)

	def __str__(self):
		return f"Корзина для {self.user.username} | Продукты {self.product.name}"

	def sum(self):
		return self.product.price * self.quantity

	def general_quantity(self):
		total_count = 0
		for basket in Basket.objects.filter(user=self):
			total_count += basket.quantity
		return total_count

	def total_cost(self):
		total_sum = 0
		for basket in Basket.objects.filter(user=self):
			total_sum += basket.sum()
		return total_sum


