from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'premasys.views.home', name='home'),
                       # url(r'^premasys/', include('premasys.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'', include("common.urls")),
                       url(r"^reveal/", include("reveal.urls")),
                       url(r'^accounts/', include('registration.backends.default.urls')),
                       url(r'^user/', include("users.urls")),
                       url(r'^moodle/', include("moodle_auth.urls")),
                       )
