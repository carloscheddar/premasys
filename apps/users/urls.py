from django.conf.urls import patterns, url
from users.views import Profile

urlpatterns = patterns("",
                       url(r'^(?P<user_id>\d+)$', Profile, name='user_url')
                       )
