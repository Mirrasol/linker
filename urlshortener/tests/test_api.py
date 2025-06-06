from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from urls.models import URL


class APITestCase(APITestCase):
    fixtures = ['urls.json', 'users.json']

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.get(id=2)
        self.url1 = URL.objects.get(pk=1)
        self.url2 = URL.objects.get(pk=2)
        self.url3 = URL.objects.get(pk=3)

    def test_read_users_list_unauthenticated(self):
        self.client.logout()

        url = reverse_lazy('api_users_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_users_list_authenticated(self):
        self.client.force_login(self.user)

        url = reverse_lazy('api_users_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_read_url_list_unauthenticated(self):
        self.client.logout()
        
        url = reverse_lazy('api_urls_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_read_url_list_authenticated(self):
        self.client.force_login(self.user)
        
        url = reverse_lazy('api_urls_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data, len(response.data) == 1)
        self.assertEqual(response.data[0]['url'], self.url3.url)
    
    def test_create_unauthenticated(self):
        self.client.logout()
        
        url = reverse_lazy('api_shorten_url')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_authenticated(self):
        self.client.force_login(self.user)

        data = {"url": "https://www.larian.com/"}
        url = reverse_lazy('api_shorten_url')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data, "hash" in response.data)
        self.assertEqual(URL.objects.get(pk=5).url, data['url'])
    
    def test_create_invalid_url(self):
        self.client.force_login(self.user)

        data = {"url": "owly"}
        url = reverse_lazy('api_shorten_url')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
