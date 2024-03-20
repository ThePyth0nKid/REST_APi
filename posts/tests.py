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
        
    
    def test_logged_in_user_can_create_post(self):
        testuser = User.objects.get(username='testuser')
        self.client.force_login(testuser)
        response = self.client.post('/posts/', {'title': 'Test Post'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'Test Post')
        
        
    def test_user_not_logged_in_cannot_create_post(self):
        response = self.client.post('/posts/', {'title': 'Test Post'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 0)
        
        
class PostDetailViewTest(APITestCase):
    def setUp(self):
        testuser = User.objects.create(username='testuser', password='pass')
        testuser2 = User.objects.create(username='testuser2', password='pass')
        Post.objects.create(owner=testuser, title='Test Post')
        Post.objects.create(owner=testuser2, title='Test Post 2')
    
    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'Test Post')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_cannot_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        
    def test_can_update_post_if_owner(self):
        self.client.force_login(User.objects.get(username='testuser'))
        response = self.client.put('/posts/1/', {'title': 'Updated Post'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Post')
        
    def test_cannot_update_post_if_not_owner(self):
        self.client.force_login(User.objects.get(username='testuser'))
        response = self.client.put('/posts/2/', {'title': 'Updated Post'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')
        