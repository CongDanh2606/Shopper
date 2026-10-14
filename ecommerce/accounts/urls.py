from django.urls import path
from . import views

urlpatterns = [
    path('account/update/', views.update_account_view, name='account_update')
]