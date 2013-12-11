from django.conf.urls import patterns, url

from tracker import views

urlpatterns = patterns('',

    # e.g. /tracker/users.json
    url(r'users.json$', views.get_users, name='get-users'),

    # e.g. /tracker/user/2/activities.json
    url(r'user/(?P<user_id>\d+)/activities.json$',
        views.get_activities_by_user, name='get-activities-by-user'
    ),
    # e.g. /tracker/ch/1/delta
    url(r'ch/(?P<ch_id>\d+)/delta$',
        views.get_delta_by_ch, name='get-delta-by-ch'
    ),
)
