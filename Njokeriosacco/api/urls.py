from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = {
    url(r'^', views.homepage, name="homepage"),
}

urlpatterns = format_suffix_patterns(urlpatterns)