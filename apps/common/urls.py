from django.conf.urls import patterns, url
from common.views import Common

urlpatterns = patterns("",
    url(r"^$", Common, name="base")
)
