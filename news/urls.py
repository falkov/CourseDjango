from django.urls import path

from .views import *

urlpatterns = [
    path("", PostList.as_view(), name="posts_list"),
    path("category/<slug:slug>/", PostList.as_view(), name="category_posts_list"),
    path("<slug:slug>/", PostDetail.as_view(), name="post_detail"),
]
