from django.conf.urls import patterns, url
from reveal.views import Reveal

urlpatterns = patterns("",
    url(r"^$", Reveal, name="presentation_view")
)
