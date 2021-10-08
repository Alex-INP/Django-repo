from django.shortcuts import render

# Create your views here.

from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.forms import inlineformset_factory
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
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

	def get_context_data(self, **kwargs):
		context = super(OrderCreate, self).get_context_data(**kwargs)
		context["title"] = "Geekshop - Создать заказ"
		OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)
		if self.request.POST:
			formset = OrderFormSet(self.request.POST)
		else:
			basket_items = Basket.objects.filter(user=self.request.user)
			if basket_items:
				OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=basket_items.count())
				formset = OrderFormSet()
				for num, form in enumerate(formset.forms):
					form.initial["product"] = basket_items[num].product
					form.initial["quantity"] = basket_items[num].quantity
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
			formset = OrderFormSet(instance=self.object)

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