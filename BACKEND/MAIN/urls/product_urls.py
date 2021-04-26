from django.urls import path
from MAIN.views import product_views

urlpatterns = [
    path("get/", product_views.getProduct, name="get-product"),
    path("getall/", product_views.getProducts, name="get-products"),
    path("edit/", product_views.editProduct, name="edit-product"),
    path("create/", product_views.createProduct, name="create-product"),
    path("delete/", product_views.deleteProduct, name="delete-product"),
]
