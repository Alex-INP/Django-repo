from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page, never_cache

import datetime
from .models import ProductCategory, Product
from geekshop import settings
# Create your views here.

def get_links_category():
	if settings.LOW_CACHE:
		key = "links_category"
		links_category = cache.get(key)

		if links_category is None:
			links_category = ProductCategory.objects.filter(is_active=True).select_related()
			cache.set(key, links_category)
		return links_category
	else:
		return ProductCategory.objects.filter(is_active=True)

def get_links_product():
	if settings.LOW_CACHE:
		key = "links_product"
		links_product = cache.get(key)

		if links_product is None:
			links_product = Product.objects.filter(is_active=True).select_related()
			cache.set(key, links_product)
		return links_product
	else:
		return Product.objects.filter(is_active=True)

def get_product(pk):
	if settings.LOW_CACHE:
		key = f"product{pk}"
		product = cache.get(key)

		if product is None:
			product = get_object_or_404(Product, pk=pk)
			cache.set(key, product)
		return product
	else:
		return get_object_or_404(Product, pk=pk)


# @never_cache
# @cache_page(3600)

def index(request):
	content = {"date": datetime.datetime.now().strftime("%d %B %Y")}
	return render(request, "index.html", content)


class ProductsShow(ListView):
	model = Product
	template_name = "products/products.html"
	paginate_by = 3

	def get_context_data(self, *, object_list=None, **kwargs):
		id = self.kwargs["pk"] if "pk" in self.kwargs.keys() else None
		if id is not None:
			self.object_list = Product.objects.filter(category=id).select_related("category")
		else:
			self.object_list = Product.objects.all().select_related("category")

		if not settings.LOCAL_HOST_DEVELOP:
			self.object_list = get_links_product()

		context = super(ProductsShow, self).get_context_data(**kwargs)
		context["categories"] = get_links_category()
		return context


class DetailProduct(DetailView):
	context_object_name = "product"
	template_name = "products/detail-product.html"
	model = Product

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["product"] = get_product(self.kwargs.get("pk"))
		return context


# ---------------------------------------Old FBV---------------------------------------

# def products(request, id=None, page=1):
# 	content = {"date": datetime.datetime.now().strftime("%d %B %Y")}
# 	products = Product.objects.filter(category=id) if id is not None else Product.objects.all()
# 	paginator = Paginator(products, per_page=3)
# 	try:
# 		products_paginator = paginator.page(page)
# 	except PageNotAnInteger:
# 		products_paginator = paginator.page(1)
# 	except EmptyPage:
# 		products_paginator = paginator.page(paginator.num_pages)
#
# 	content["goods"] = products_paginator
# 	content["categories"] = ProductCategory.objects.all()
# 	return render(request, "products.html", content)