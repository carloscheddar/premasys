from django.conf.urls import patterns, url
from common.views import Common, Login

urlpatterns = patterns("",
    url(r"^$", Common, name="base"),
    url(r"^login/", Login, name="login")
)
