from django.urls import path

from .views import *

urlpatterns = [
    path("", PostList.as_view(), name="posts_list"),
    path("search/", SearchForCategoryAndTitleList.as_view(), name='search_category_title_list'),
    path("search_days/<int:days_amount>", SearchForDateList.as_view(), name='search_days_list'),
    path("category/<slug:slug>/", PostList.as_view(), name="category_posts_list"),
    path("<slug:slug>/", PostDetail.as_view(), name="post_detail"),
]
