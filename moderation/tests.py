from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch
from .models import FlaggedContent


class FirebaseAuthTest(APITestCase):
    def setUp(self):
        # Setup mock Firebase authentication
        self.mock_firebase_patcher = patch(
            "firebase_admin.auth.verify_id_token"
        )
        self.mock_firebase = self.mock_firebase_patcher.start()
        self.mock_firebase.return_value = {"uid": "testfirebaseuid"}

        # Create a test user associated with the Firebase uid
        self.client = APIClient()
        self.token = "mocked.firebase.jwt.token"
        self.invalid_token = "invalid.token"
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def tearDown(self):
        self.mock_firebase_patcher.stop()

    def test_valid_firebase_auth(self):
        """Ensure Firebase authentication works with a valid token"""
        response = self.client.get(
            reverse("flaggedcontent-list")
        )  # DRF view for FlaggedContent
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_firebase_auth(self):
        """Ensure invalid Firebase tokens dont raise an error"""
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.invalid_token}"
        )
        response = self.client.get(reverse("flaggedcontent-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_flagged_content_valid(self):
        """posting content with trigger words using valid Firebase token"""
        post_data = {
            "content": "This post contains kms, a trigger word",
            "user": "testfirebaseuid",
            "post_id": "12345",
            "reason": "Trigger words detected",
        }
        response = self.client.post(
            reverse("flaggedcontent-list"), post_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FlaggedContent.objects.count(), 1)

    def test_post_flagged_content_invalid_token(self):
        """Ensure posting invalid Firebase token allows content creation"""
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.invalid_token}"
        )
        post_data = {
            "content": "This post contains kms, a trigger word",
            "user": "testfirebaseuid",
            "post_id": "12345",
            "reason": "Trigger words detected",
        }
        response = self.client.post(
            reverse("flaggedcontent-list"), post_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_safe_content(self):
        """Test posting safe content that doesn't contain trigger words"""
        post_data = {
            "content": "This is a safe post with no trigger words",
            "user": "testfirebaseuid",
            "post_id": "54321",
            "reason": "Safe content",
        }
        response = self.client.post(
            reverse("flaggedcontent-list"), post_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_flagged_content_list(self):
        """Test getting a list of flagged content"""
        FlaggedContent.objects.create(
            user="testfirebaseuid",
            post_id="12345",
            reason="Trigger words detected",
            content="Test post containing kms",
        )

        response = self.client.get(reverse("flaggedcontent-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0].get("content", ""), "Test post containing kms"
        )
