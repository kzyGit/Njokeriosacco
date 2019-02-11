from django.urls import reverse
from rest_framework.views import status
import json
from basetest import BaseViewTest


class SavingsTest(BaseViewTest):

    # Add savings for a user
    def create_savings(self):
        return self.client.post(
            reverse('savings', kwargs={'pk': self.user.id}),
            data=json.dumps({"amount": 2000}),
            content_type="application/json")

    # Get all user savings

    def savings(self):
        return self.client.get(
            reverse('savings', kwargs={'pk': self.user.id}), format='json')

    # Get user single savings
    def single_saving(self):
        return self.client.get(
            reverse(
                'single_saving',
                kwargs={'pk': SavingsTest.savings(self).data['data'][0]['id']}),
            format='json')

    def test_admin_can_add_savings_for_a_user(self):
        self.assertEqual(self.savings.status_code, status.HTTP_201_CREATED)

    def test_non_admin_cannot_add_a_user_savings(self):
        self.login_client("user@mail.com", "user@mail.com")
        res = self.client.post(
            reverse('savings', kwargs={'pk': self.user.id}),
            format='json',
            data=json.dumps({'amount': 100}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_savings_with_incomplete_input(self):
        res = self.client.post(
            reverse('savings', kwargs={'pk': self.user.id}),
            format='json',
            data=json.dumps({}))
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_can_get_all_savings_for_a_user(self):
        self.assertEqual(
            SavingsTest.savings(self).status_code, status.HTTP_200_OK)

    def test_admin_can_get_a_single_saving_detail_for_a_user(self):
        self.assertEqual(
            SavingsTest.single_saving(self).status_code, status.HTTP_200_OK)

    def test_admin_can_update_a_single_saving_detail_for_a_user(self):
        self.client.put(
            reverse(
                'single_saving',
                kwargs={'pk': SavingsTest.savings(self).data['data'][0]['id']}),
            data={'amount': 100},
            format='json')
        saving = SavingsTest.single_saving(self)
        self.assertEqual(saving.data['amount'], 100)

    def test_admin_can_delete_a_single_saving_detail_for_a_user(self):
        res = self.client.delete(
            reverse(
                'single_saving',
                kwargs={'pk': SavingsTest.savings(self)
                        .data['data'][0]['id']}))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
