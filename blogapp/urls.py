from django.urls import path
from .views import *

urlpatterns = [
    path('',home, name='home'),
    path('news/', news, name='news'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutPage, name='logout'),
    path('register/', registerPage, name='register'),
    path('add-blog/', add_blog, name='add_blog'),
    path('blog-detail/<slug>', blog_detail, name='blog_detail'),
    path('see-blog/', see_blog, name='see_blog'),
    path('blog-delete/<int:id>', blog_delete, name='blog_delete'),
    path('blog-update/<str:slug>', blog_update, name='blog_update'),
    path('news/', news, name='news'),

]
