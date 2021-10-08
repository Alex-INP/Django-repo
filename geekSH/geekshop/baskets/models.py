from django.db import models

from users.models import NormalUser
from products.models import Product


# Create your models here.

# class BasketQuerySet(models.QuerySet):
#
# 	def delete(self, *args, **kwargs):
# 		for item in self:
# 			item.product.quantity += item.quantity
# 			item.product.save()
# 		super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
	# objects = BasketQuerySet.as_manager()
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
		for basket in Basket.objects.filter(user=self.user):
			total_count += basket.quantity
		return total_count

	def total_cost(self):
		total_sum = 0
		for basket in Basket.objects.filter(user=self.user):
			total_sum += basket.sum()
		return total_sum

	@staticmethod
	def get_item(pk):
		return Basket.objects.get(pk=pk).quantity

	# def delete(self, *args, **kwargs):
	# 	self.product.quantity += self.quantity
	# 	self.save()
	# 	super(Basket, self).delete(*args, **kwargs)
	#
	# def save(self, *args, **kwargs):
	# 	if self.pk:
	# 		self.product.quantity -= self.quantity - self.get_item(self.pk)
	# 	else:
	# 		self.product.quantity -= self.quantity
	# 	self.product.save()
	# 	super(Basket, self).save(*args, **kwargs)

