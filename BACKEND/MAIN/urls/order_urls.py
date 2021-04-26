from django.urls import path
from MAIN.views import order_views

urlpatterns = [
    path("get/", order_views.getOrder, name="get-order"),
    path("getall/", order_views.getOrders, name="get-orders"),
    path("edit/", order_views.editOrder, name="edit-order"),
    path("create/", order_views.createOrder, name="create-order"),
]
