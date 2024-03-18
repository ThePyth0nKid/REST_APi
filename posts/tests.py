from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Post
from .serializers import PostSerializer

class PostDetailTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='testuser', password='pass')

    def test_can_list_posts(self):
        testuser = User.objects.get(username='testuser')
        Post.objects.create(owner=testuser, title='Test Post')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))
    
    def test_logged_in_user_can_create_post(self):
        testuser = User.objects.get(username='testuser')
        self.client.force_login(testuser)
        response = self.client.post('/posts/', {'title': 'Test Post'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'Test Post')
        print(response.data)
        
    def test_user_not_logged_in_cannot_create_post(self):
        response = self.client.post('/posts/', {'title': 'Test Post'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 0)
        print(response.data)