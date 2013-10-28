from django.conf.urls import patterns, url
from reveal.views import Reveal, Edit, Save, Create, Show

urlpatterns = patterns("",
    url(r"^$", Reveal, name="presentation_view"),
    url(r"create", Create, name="Create View"),
    url(r"edit/(?P<lesson_id>\d+)$", Edit, name="Edit View"),
    url(r"save", Save, name="Save View"),
    url(r"show/(?P<lesson_id>\d+)$", Show, name="Show View"),
)
