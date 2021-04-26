from django.urls import path
from MAIN.views import user_views 

urlpatterns = [
    path("get/", user_views.getUser, name="get-user"), 
    path("getall/", user_views.getUsers, name="get-users"),
    path("edit/", user_views.editUser, name="edit-user"),
    path("register/", user_views.registerUser, name="create-user"),
    path("delete/", user_views.deleteUser, name="delete-user"),
]

