from django.urls import path
from . import views

urlpatterns = [
    path('account/my-product/', views.my_product_view, name='my_product'),
    path('account/add-product/', views.add_product_view, name='add_product'),
]