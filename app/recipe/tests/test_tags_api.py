"""
Test for the tags API.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

def detail_url(tag_id):
    """Create and return a tag detail URL"""
    return reverse('recipe:tag-detail', args=[tag_id])


def create_user(email='user@example.com', password='sample123'):
    """Function to create a test user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicTagAPITests(TestCase):
    """Test unauthenticate API request."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):
    """Test authenticate API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retieving a list of tags."""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Breakfast')

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_list_limited_to_user(self):
        """Test list of tags limited by the user authenticated"""
        other_user = create_user(email='example2@example.com', password='test123')
        Tag.objects.create(user=other_user, name='Lunch')

        tag = Tag.objects.create(user=self.user, name='Celiac')

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)

    def test_update_tag(self):
        """Test update a tag"""
        tag = Tag.objects.create(user=self.user, name='Vegan')
        url = detail_url(tag.id)

        payload = {'name': 'Fast Food'}

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    def test_delete_tag(self):
        """Test deleting a tag successfully"""
        tag = Tag.objects.create(user=self.user, name='Breakfast')

        url = detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tag.objects.filter(id=tag.id).exists())