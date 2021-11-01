from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import Q
from admins.views import db_profile_by_type
from django.db.models import F, When, Case, DecimalField, IntegerField
from datetime import timedelta

from ordersapp.models import OrderItem


class Command(BaseCommand):
	def handle(self, *args, **options):
		ACTION_1 = 1
		ACTION_2 = 2
		ACTION_3 = 3

		action_1_time_delta = timedelta(hours=12)
		action_2_time_delta = timedelta(days=1)

		action_1_discount = 0.3
		action_2_discount = 0.15
		action_3_discount = 0.05

		action_1_condition = Q(order__updated__lte=F('order__created') + action_1_time_delta)
		action_2_condition = Q(order__updated__gt=F('order__created') + action_1_time_delta) & Q(order__updated__lte=F('order__created') + action_2_time_delta)
		action_3_condition = Q(order__updated__gt=F('order__created') + action_2_time_delta)

		action_1_order = When(action_1_condition, then=ACTION_1)
		action_2_order = When(action_2_condition, then=ACTION_2)
		action_3_order = When(action_3_condition, then=ACTION_3)

		action_1_price = When(action_1_condition, then=F('product__price') * F('quantity') * action_1_discount)
		action_2_price = When(action_2_condition, then=F('product__price') * F('quantity') * -action_2_discount)
		action_3_price = When(action_3_condition, then=F('product__price') * F('quantity') * action_3_discount)

		test_orders = OrderItem.objects.annotate(
			action_order=Case(
				action_1_order,
				action_2_order,
				action_3_order,
				output_field=IntegerField(),
			)).annotate(
			total_price=Case(
				action_1_price,
				action_2_price,
				action_3_price,
				output_field=DecimalField(),
			))

		for order in test_orders:
			print(f"{order.order} ||| Товар: {order.product} ||| Действие: {order.action_order} ||| Цена: {order.total_price} ||| Скидка: {order.product.price - order.total_price}")
