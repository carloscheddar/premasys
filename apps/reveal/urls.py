from django.conf.urls import patterns, url
from reveal.views import Reveal, Edit, Save

urlpatterns = patterns("",
    url(r"^$", Reveal, name="presentation_view"),
    url(r"edit", Edit, name="Edit View"),
    url(r"save", Save, name="Save View"),
)
