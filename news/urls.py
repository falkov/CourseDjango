from django.urls import path

from .views import *

urlpatterns = [
    path("<int:post_number>/", PostDetail.as_view()),
    path("", PostList.as_view()),
]
