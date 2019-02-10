from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls import url, include
from django.contrib import admin
from .views import LoginView, Users, UserDetailsView, LogoutView, SavingsView, SavingsDetailsView

urlpatterns = [
    url(r'^login/', LoginView.as_view(), name="login"),
    url(r'^logout/', LogoutView, name="logout"),
    url(r'^users/', Users.as_view(), name="auth-register"),
    url(r'^user/(?P<pk>[0-9]+)/', UserDetailsView.as_view(), name="user"),
    url(r'^api-token-auth/', obtain_jwt_token, name='create-token'),
    url(r'^savings/(?P<pk>[0-9]+)/', SavingsView.as_view(), name="savings"),
    url(r'^single_saving/(?P<pk>[0-9]+)/', SavingsDetailsView.as_view(), name="single_saving")
]