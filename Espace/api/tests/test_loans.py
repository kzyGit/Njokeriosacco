from django.urls import reverse
from rest_framework.views import status
import json
from basetest import BaseViewTest


class LoansTest(BaseViewTest):

    # Add loan for a user
    def create_loan(self):
        return self.client.post(
            reverse('loans', kwargs={'pk': self.user.id}),
            data=json.dumps({"amount": 2000}),
            content_type="application/json")

    # Get user loan

    def loan(self):
        return self.client.get(
            reverse('loans', kwargs={'pk': self.user.id}), format='json')

    def test_admin_can_add_loan_for_a_user(self):
        self.assertEqual(self.loan.status_code, status.HTTP_201_CREATED)

    def test_non_admin_cannot_add_a_user_savings(self):
        self.login_client("user@mail.com", "user@mail.com")
        res = self.client.post(
            reverse('loans', kwargs={'pk': self.user.id}),
            format='json',
            data=json.dumps({'amount': 1000}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_get_all_loans_for_a_user(self):
        self.assertEqual(LoansTest.loan(self).status_code, status.HTTP_200_OK)

    def test_admin_can_get_a_single_loan_detail_for_a_user(self):
        self.assertEqual(LoansTest.loan(self).status_code, status.HTTP_200_OK)

    def test_admin_can_update_a_single_loan_detail_for_a_user(self):
        res = self.client.put(
            reverse(
                'single_loan',
                kwargs={'pk': LoansTest.loan(self).data[0]['id']}),
            data={'amount': 100},
            format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_can_delete_a_single_loan_detail_for_a_user(self):
        res = self.client.delete(
            reverse(
                'single_loan',
                kwargs={'pk': LoansTest.loan(self).data[0]['id']}))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
