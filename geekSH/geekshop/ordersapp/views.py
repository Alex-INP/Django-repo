from django.shortcuts import render

# Create your views here.

from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.forms import inlineformset_factory
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete, post_save

from baskets.models import Basket
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemsForm


class OrderList(ListView):
	model = Order

	def get_queryset(self):
		return Order.objects.filter(user=self.request.user, is_active=True)


class OrderCreate(CreateView):
	model = Order
	fields = []
	success_url = reverse_lazy("orders:list")
	# template_name = "ordersapp/order_form.html"

	def get_context_data(self, **kwargs):
		context = super(OrderCreate, self).get_context_data(**kwargs)
		context["title"] = "Geekshop - Создать заказ"
		OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)
		if self.request.POST:
			formset = OrderFormSet(self.request.POST)
		else:
			basket_items = Basket.objects.filter(user=self.request.user)
			if basket_items:
				context["total_quantity"] = basket_items[0].general_quantity()
				context["total_cost"] = basket_items[0].total_cost()

				OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=basket_items.count())
				formset = OrderFormSet()
				for num, form in enumerate(formset.forms):
					form.initial["product"] = basket_items[num].product
					form.initial["quantity"] = basket_items[num].quantity
					form.initial["price"] = basket_items[num].product.price
				basket_items.delete()
			else:
				formset = OrderFormSet()

		context["orderitems"] = formset

		return context

	def form_valid(self, form):
		context = self.get_context_data()
		orderitems = context["orderitems"]

		with transaction.atomic():
			form.instance.user = self.request.user
			self.object = form.save()

			if orderitems.is_valid():
				orderitems.instance = self.object
				orderitems.save()

			if self.object.get_total_cost() == 0:
				self.object.delete()

			return super().form_valid(form)


class OrderUpdate(UpdateView):
	model = Order
	fields = []
	success_url = reverse_lazy("orders:list")

	def get_context_data(self, **kwargs):
		context = super(OrderUpdate, self).get_context_data(**kwargs)
		context["title"] = "Geekshop - Создать заказ"
		OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)
		if self.request.POST:
			formset = OrderFormSet(self.request.POST, instance=self.object)
		else:
			queryset =self.object.orderitems.select_related()
			formset = OrderFormSet(instance=self.object, queryset=queryset)
			for form in formset:
				if form.instance.pk:
					form.initial["price"] = form.instance.product.price

		context["orderitems"] = formset
		return context

	def form_valid(self, form):
		context = self.get_context_data()
		orderitems = context["orderitems"]

		with transaction.atomic():
			self.object = form.save()
			if orderitems.is_valid():
				orderitems.instance = self.object
				orderitems.save()

			if self.object.get_total_cost() == 0:
				self.object.delete()

			return super().form_valid(form)


class OrderDelete(DeleteView):
	model = Order
	success_url = reverse_lazy("orders:list")


class OrderRead(DetailView):
	model = Order

	def get_context_data(self, **kwargs):
		context = super(OrderRead, self).get_context_data(**kwargs)
		context["title"] = "Geekshop - Создать заказ"
		return context


class OrderItemsCreate(CreateView):
	pass


def order_forming_complete(request, pk):
	order = get_object_or_404(Order, pk=pk)
	order.status = order.SENT_TO_PROCEED
	order.save()
	return HttpResponseRedirect(reverse("orders:list"))


@receiver(pre_save, sender=OrderItem)
# @receiver(pre_save, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):

	# print(f"{instance=}")
	# print(f"{int(instance.quantity)=}")
	# print(f"{instance.get_item(instance.pk)=}")
	# print(f"{instance.product.quantity=}")
	# if sender == Basket and instance.pk:

	if instance.pk:
		instance.product.quantity -= instance.quantity - instance.get_item(instance.pk)
	else:
		instance.product.quantity -= instance.quantity

	# print(f"{instance.product.quantity=}")

	instance.product.save()
	# print("product_quantity_update_SAVE")

@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
	instance.product.quantity += instance.quantity
	instance.product.save()
	# print("product_quantity_update_DELETE")



