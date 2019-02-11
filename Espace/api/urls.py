from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls import url
from .views import (LoginView, Users, UserDetailsView, LogoutView, SavingsView,
                    SavingsDetailsView, LoansApiView, LoansDetailsView,
                    LoansRepaymentsView, LoansRepaymentsDetailsView)

urlpatterns = [
    url(r'^login/', LoginView.as_view(), name="login"),
    url(r'^logout/', LogoutView, name="logout"),
    url(r'^users/', Users.as_view(), name="auth-register"),
    url(r'^user/(?P<pk>[0-9]+)/', UserDetailsView.as_view(), name="user"),
    url(r'^api-token-auth/', obtain_jwt_token, name='create-token'),
    url(r'^savings/(?P<pk>[0-9]+)/', SavingsView.as_view(), name="savings"),
    url(r'^savings/', SavingsView.as_view(), name="all_savings"),
    url(r'^single_saving/(?P<pk>[0-9]+)/',
        SavingsDetailsView.as_view(),
        name="single_saving"),
    url(r'^loans/(?P<pk>[0-9]+)/', LoansApiView.as_view(), name="loans"),
    url(r'^loans/', LoansApiView.as_view(), name="all_loans"),
    url(r'^single_loan/(?P<pk>[0-9]+)/',
        LoansDetailsView.as_view(),
        name="single_loan"),
    url(r'^repayment/(?P<pk>[0-9]+)/',
        LoansRepaymentsView.as_view(),
        name="repayment"),
    url(r'^single_repayment/(?P<pk>[0-9]+)/',
        LoansRepaymentsDetailsView.as_view(),
        name="single_repayment")
]
