from django.shortcuts import render

import datetime
from .models import ProductCategory, Product
# Create your views here.


def index(request):
	content = {"date": datetime.datetime.now().strftime("%d %B %Y")}
	return render(request, "index.html", content)

def products(request):
	content = {"date": datetime.datetime.now().strftime("%d %B %Y")}
	content["category_names"] = list(reversed([i.name for i in ProductCategory.objects.all()]))
	goods_list = []
	for i in Product.objects.all():
		goods_list.append({
		"name": i.name,
		"image": i.image,
		"description": i.description,
		"price": i.price
		})
	content["goods"] = goods_list

	return render(request, "products.html", content)
