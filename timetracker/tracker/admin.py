from timetracker.tracker.models import CostHolder,Activity

from django.contrib import admin
from django.conf.urls import patterns
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from datetime import datetime

class ActivityAdmin(admin.ModelAdmin):
    #WAS: list_display = ('__unicode__','cost_holder','start_datetime','end_datetime')
 
    list_display = (
        'pk', '__unicode__','cost_holder', 
        'starttime_button', 'start_datetime',
        'end_datetime',
    )
    list_editable = ('start_datetime', 'end_datetime')
   
    def starttime_button(self,obj):
        start_time = obj.start_datetime

        if start_time:
            out = "<span activity-id=\"%s\" id=\"start_%d\" class=\"started\" >STARTED</span>" % (obj.pk, obj.pk)
        else:
            #WAS: out = "<a id=\"start\" onclick=\"start()\" href=\"start_activity/%d\">START</a>" % obj.pk
            out = "<span activity-id=\"%s\" id=\"start_%d\" class=\"start\" onclick=\"start();\" >START</span>" % (obj.pk, obj.pk)

        return out

    starttime_button.allow_tags = True

    def get_urls(self):
        urls = super(ActivityAdmin, self).get_urls()
        my_urls = patterns('',
        (r'^start_activity/(?P<activity_id>\d+)/$', self.admin_site.admin_view(self.starttime_button_view))
        )
        return my_urls + urls

    #@login_required
    def starttime_button_view(self, request, activity_id):
        print "manina cliccatina"
        activity = get_object_or_404(Activity, pk=activity_id)
        activity.start_datetime = datetime.now()
        activity.save()
        return HttpResponse("Complimenti, hai appena aggiunto lo start_time alla tua activity :3 !!! Lo start_time ora vale:%s\n%s" % (activity.start_datetime,"<a href=\"../..\"> back </a>"))

    def queryset(self, request):
        qs = super(ActivityAdmin, self).queryset(request)
        #if request.user.is_superuser:
        #    return qs
        user_cost_holders = request.user.costholder_set.all()
        return qs.filter(
            cost_holder__in=user_cost_holders,
            user=request.user
        )

    def changelist_view(self, request, extra_context=None):
        user = request.user
        for ch in user.costholder_set.all():
            act, created = Activity.objects.get_or_create(
                cost_holder=ch, 
                user=user, 
                start_datetime__isnull = True
            )
            print(act, created)

        # Restrict rows to costholders belonging to user
        rv = super(ActivityAdmin, self).changelist_view(request, extra_context=extra_context)
        return rv

admin.site.register(CostHolder)
admin.site.register(Activity, ActivityAdmin)

