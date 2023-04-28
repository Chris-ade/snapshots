from django.urls import path
from . import views

app_name = "feed"

urlpatterns = [
    path('', views.feed, name='home'),
    path('upload', views.upload, name='upload'),
    path('like', views.like, name='like'),
    path('like/comment', views.likeComment, name='like-comment'),
    path('comment', views.comment, name='comment'),
    path('<str:link>', views.view, name='view'),
]
