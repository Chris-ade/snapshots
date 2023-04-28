from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('user/<username>', views.profile, name='profile'),
    path('user/<username>/feeds', views.feeds, name='feeds'),
    path('user/<username>/comments', views.comments, name='comments'),
    path('user/<username>/images', views.images, name='images'),
    path('user/<username>/videos', views.videos, name='videos'),
]
