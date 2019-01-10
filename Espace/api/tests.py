from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import User
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
        self.response = self.client.get(
            reverse('user',
            kwargs={'pk': self.user.id}), format="json")


class UserTestView(BaseViewTest):

    def test_admin_can_register_a_user(self):
        self.assertEqual(self.create_user.status_code, status.HTTP_201_CREATED)

    def test_non_admin_cannot_create_a_user(self):
        self.login_client("user@mail.com", "user@mail.com")
        res = self.client.post(
            reverse('auth-register'), data=json.dumps(self.new_user2),content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_register_a_user_with_incomplete_input(self):
        res = self.client.post(
            reverse('auth-register'), 
            data=json.dumps({
                "email":"",
                "first_name":""
                }),
            content_type="application/json")
            
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_a_duplicate_user(self):
        res = self.client.post(
            reverse('auth-register'), data=json.dumps(self.new_user),content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_can_get_a_user(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertContains(self.response, self.user)

    def test_update_a_user(self):
        new_info = {
            'email':'user1@mail.com',
            'first_name':'first1',
            'middle_name':'middle1',
            'sur_name':'sur_name1',
            'id_number':1234571}
        response = self.client.put(
            reverse('user', kwargs={'pk':self.user.id}), new_info, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_delete_a_user(self):
        response = self.client.delete(
            reverse('user', kwargs={'pk':self.user.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class AuthLoginViewTest(BaseViewTest):
    def test_user_can_login(self):
        res = self.login_a_user("user@mail.com", "user@mail.com")
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.login_a_user("anonymous", "testing")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)