from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from api.models import Savings, User
import json

class BaseViewTest(APITestCase):
    client = APIClient()
    

    def login_a_user(self, username="", password=""):
        url = reverse("login")
        return self.client.post(
            url, 
            data=json.dumps({ "username":username, "password":password}),content_type="application/json")
            
    def login_client(self, username="", password=""):
        url = reverse("login")
        response = self.client.post(
            url,
            data=json.dumps({'username': username, 'password': password}), content_type='application/json')

        self.token = response.data['token']
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        return self.token

    def setUp(self):
        self.admin = User.objects.create_superuser(
            email="admin@mail.com",
            first_name="first",
            middle_name="middle",
            sur_name="sur_name",
            id_number=123456,
            password="admin@mail.com"
        )
        self.new_user = {'email':'user@mail.com',
            'first_name':'first',
            'middle_name':'middle',
            'sur_name':'sur_name',
            'id_number':123457}

        self.new_user2 = {'email':'user2@mail.com',
            'first_name':'first',
            'middle_name':'middle',
            'sur_name':'sur_name',
            'id_number':123458}

        # Admin login and create a new user
        self.login_client("admin@mail.com", "admin@mail.com")
        self.create_user = self.client.post(
            reverse('auth-register'), data=json.dumps(self.new_user),content_type="application/json")

        # Get a single user
        self.user = User.objects.get(is_staff=True)
        self.single_user = self.client.get(
            reverse('user',
            kwargs={'pk': self.user.id}), format="json")

        # Add savings for a user
        self.savings = self.client.post(
            reverse('savings', kwargs={'pk':self.user.id}), data=json.dumps({"amount":2000}), content_type="application/json")

