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
from admins.views import index, UserListView, UserCreateView, UserUpdateView, UserDeleteView, \
	CategoryListView, CategoryUpdateView, CategoryCreateView, CategoryDeleteView, ProductListView, \
	ProductCreateView, ProductUpdateView, ProductDeleteView

# from admins.views import index, admin_users, admin_users_create, admin_users_update, admin_users_delete, \
# 	admin_category_show, admin_category_update, admin_category_create, admin_category_delete, admin_product_show, \
# 	admin_product_create, admin_product_update, admin_product_delete

app_name = "admins"

urlpatterns = [
	path("", index, name="index"),
	path("users/", UserListView.as_view(), name="admin_users"),
	path("user_create/", UserCreateView.as_view(), name="admin_users_create"),
	path("user_update/<int:pk>", UserUpdateView.as_view(), name="admin_users_update"),
	path("user_delete/<int:pk>", UserDeleteView.as_view(), name="admin_users_delete"),
	path("category_show", CategoryListView.as_view(), name="admin_category_show"),
	path("category_create/", CategoryCreateView.as_view(), name="admin_category_create"),
	path("category_update/<int:pk>", CategoryUpdateView.as_view(), name="admin_category_update"),
	path("category_delete/<int:pk>", CategoryDeleteView.as_view(), name="admin_category_delete"),
	path("product_show/", ProductListView.as_view(), name="admin_product_show"),
	path("product_create/", ProductCreateView.as_view(), name="admin_product_create"),
	path("product_update/<int:pk>", ProductUpdateView.as_view(), name="admin_product_update"),
	path("product_delete/<int:pk>", ProductDeleteView.as_view(), name="admin_product_delete"),
]
