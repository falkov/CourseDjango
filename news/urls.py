from django.urls import path

from .views import *

urlpatterns = [
    path("", PostList.as_view(), name="posts_list"),
    path("search/", Search.as_view(), name='search_category_title'),
    path("search_days/<int:days_amount>", SearchForDate.as_view(), name='search_days'),
    path("category/<slug:slug>/", PostList.as_view(), name="category_posts_list"),
    path("<slug:slug>/", PostDetail.as_view(), name="post_detail"),
]
