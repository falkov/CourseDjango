from django.test import TestCase, Client
from django.urls import reverse

from .models import Post, Category


class MyTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.category = Category.objects.create(name="Category_name", slug="Category_slug")
        self.post = Post.objects.create(
            title="Post Title",
            text="Post Text",
            slug="Post_slug",
            category=self.category
        )

    def test_category(self):
        self.assertEqual(self.category.slug, "Category_slug")

    def test_post(self):
        self.assertEqual(self.post.title, "Post Title")

    def test_list_post(self):
        response = self.client.get(reverse('posts_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_single(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_post_single_response(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(response.context.get("post").text, "Post Text")

