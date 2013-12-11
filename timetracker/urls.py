from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'timetracker.views.home', name='home'),
    # url(r'^timetracker/', include('timetracker.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^tracker/', include('tracker.urls')),
)
