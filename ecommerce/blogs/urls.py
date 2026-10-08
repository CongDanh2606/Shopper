from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogs_view, name='blogs'),
    path('<int:id>/', views.blog_detail_view, name='blog_detail'),
    path('rate/', views.blog_rate, name='blog_rate'),
    path('comment/', views.blog_comment, name='blog_comment'),
]