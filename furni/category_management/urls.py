from django.urls import path,include
from . import views

urlpatterns = [
    path('category/',views.show_category,name='category'),
    path('addcategory/',views.add_category,name='addcategory'),
    path('editcategory/<str:id>/',views.edit_category,name='editcategory'),
    path('deletecategory/<str:id>/',views.delete_category,name='deletecategory'),
    path('category/search/',views.search,name='search'),
    
]