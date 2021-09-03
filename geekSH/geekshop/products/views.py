from django.shortcuts import render

import datetime
from .models import ProductCategory, Product
# Create your views here.


def index(request):
	content = {"date": datetime.datetime.now().strftime("%d %B %Y")}
	return render(request, "index.html", content)

def products(request):
	content = {"date": datetime.datetime.now().strftime("%d %B %Y")}
	content["category_names"] = ProductCategory.objects.all()
	content["goods"] = Product.objects.all()

	return render(request, "products.html", content)
