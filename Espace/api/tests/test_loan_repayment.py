from django.urls import reverse
import json
from basetest import BaseViewTest


class LoansRepTest(BaseViewTest):

    # Add loan for a user
    def create_loan(self):
        return self.client.post(
            reverse('loans', kwargs={'pk': self.user.id}),
            data=json.dumps({"amount": 2000}),
            content_type="application/json")
