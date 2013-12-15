from django.conf.urls import patterns, url
from moodle_auth.views import MoodleLogin, Authenticate


urlpatterns = patterns("",
                       url(r'^$', MoodleLogin, name='moodle_login'),
                       url(r'^authenticate', Authenticate, name='moodle_auth'),
                       )
