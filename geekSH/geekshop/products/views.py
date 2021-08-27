from django.shortcuts import render
import datetime
import json
from geekshop.settings import STATIC_URL
# Create your views here.


def index(request):
	content = {"date": datetime.datetime.now().strftime("%d %B %Y")}
	return render(request, "index.html", content)

def products(request):
	content = {"date": datetime.datetime.now().strftime("%d %B %Y")}

	with open("products/data.json", "r", encoding="utf-8") as file:
		content.update({"goods": json.load(file)})
	for i in content["goods"]:
		i["url"] = STATIC_URL + i["url"]
	return render(request, "products.html", content)
