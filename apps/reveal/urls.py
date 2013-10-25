from django.conf.urls import patterns, url
from reveal.views import Reveal, Edit

urlpatterns = patterns("",
    url(r"^$", Reveal, name="presentation_view"),
    url(r"edit", Edit, name="Edit View")
)
