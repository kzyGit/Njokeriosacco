from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls import url, include
from django.contrib import admin
from .views import LoginView, Users, UserDetailsView, LogoutView

urlpatterns = [
    url(r'^login/', LoginView.as_view(), name="login"),
    url(r'^logout/', LogoutView, name="logout"),
    url(r'^users/', Users.as_view(), name="auth-register"),
    url(r'^user/(?P<pk>[0-9]+)/', UserDetailsView.as_view(), name="user"),
    url(r'^api-token-auth/', obtain_jwt_token, name='create-token'),
]