from django.urls import path, include
from . import views

urlpatterns = [
    path("category/", views.show_category, name="category"),
    path("addcategory/", views.add_category, name="addcategory"),
    path("editcategory/<str:id>/", views.edit_category, name="editcategory"),
    path("search/", views.search, name="search"),
    path("listcategory/<str:id>", views.list_category, name="listcategory"),
    path("unlistcategory/<str:id>", views.un_list_category, name="unlistcategory"),
]
