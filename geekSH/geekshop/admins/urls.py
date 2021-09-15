"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from admins.views import index, admin_users, admin_users_create, admin_users_update, admin_users_delete, \
	admin_category_show, admin_category_update, admin_category_create, admin_category_delete

app_name = "admins"

urlpatterns = [
    path("", index, name="index"),
	path("users/", admin_users, name="admin_users"),
	path("user_create/", admin_users_create, name="admin_users_create"),
	path("user_update/<int:id>", admin_users_update, name="admin_users_update"),
	path("user_delete/<int:id>", admin_users_delete, name="admin_users_delete"),
	path("category_show", admin_category_show, name="admin_category_show"),
	path("category_create/", admin_category_create, name="admin_category_create"),
	path("category_update/<int:id>", admin_category_update, name="admin_category_update"),
	path("category_delete/<int:id>", admin_category_delete, name="admin_category_delete"),
]
