from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

import datetime
from .models import ProductCategory, Product
# Create your views here.


def index(request):
	content = {"date": datetime.datetime.now().strftime("%d %B %Y")}
	return render(request, "index.html", content)

class ProductsShow(ListView):
	model = Product
	template_name = "products/products.html"

	def get_context_data(self, *, object_list=None, **kwargs):
		id = self.kwargs["pk"] if "pk" in self.kwargs.keys() else None
		page = self.kwargs["page"] if "page" in self.kwargs.keys() else 1

		context = super(ProductsShow, self).get_context_data(**kwargs)
		context["date"] = datetime.datetime.now().strftime("%d %B %Y")

		products = Product.objects.filter(category=id) if id is not None else Product.objects.all()
		paginator = Paginator(products, per_page=3)
		try:
			products_paginator = paginator.page(page)
		except PageNotAnInteger:
			products_paginator = paginator.page(1)
		except EmptyPage:
			products_paginator = paginator.page(paginator.num_pages)

		context["goods"] = products_paginator
		context["categories"] = ProductCategory.objects.all()
		return context


class DetailProduct(DetailView):
	context_object_name = "product"
	template_name = "products/detail-product.html"
	model = Product


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