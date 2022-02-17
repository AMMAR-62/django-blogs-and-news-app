from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'blog', BlogViewSet)


urlpatterns = [
    path('',home, name='home'),
    path('news/', news, name='news'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutPage, name='logout'),
    path("register/", register_request, name="register"),
    path('add-blog/', add_blog, name='add_blog'),
    path('blog-detail/<slug>', blog_detail, name='blog_detail'),
    path('see-blog/', see_blog, name='see_blog'),
    path('blog-delete/<int:id>', blog_delete, name='blog_delete'),
    path('password_change/', blog_update, name='password_change'),
    path('password_change/done/ ', blog_update, name='password_change_done'),
    path('password_reset/', password_reset_request, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('news/', news, name='news'),
    path('blog/', include(router.urls)),

]

