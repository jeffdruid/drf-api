from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_can_list_posts(self):
        response = self.client.get("/posts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username="testuser", password="testpassword")
        data = {"title": "test title", "content": "test content"}
        response = self.client.post("/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, "test title")

    def test_logged_out_user_cannot_create_post(self):
        data = {"title": "test title", "content": "test content"}
        response = self.client.post("/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 0)


class PostDetailViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.post = Post.objects.create(
            title="test title", content="test content", author=self.user
        )

    def test_can_retrieve_post(self):
        response = self.client.get(f"/posts/{self.post.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "test title")

    def test_can_update_post(self):
        self.client.login(username="testuser", password="testpassword")
        data = {"title": "updated title", "content": "updated content"}
        response = self.client.put(f"/posts/{self.post.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.get().title, "updated title")

    def test_can_delete_post(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.delete(f"/posts/{self.post.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)
