from timetracker.tracker.models import CostHolder,Activity

from django.contrib import admin
from django.conf.urls import patterns
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from datetime import datetime

class ActivityAdmin(admin.ModelAdmin):
    #WAS: list_display = ('__unicode__','cost_holder','start_datetime','end_datetime')
 
    list_display = ('__unicode__','cost_holder','starttime_button','end_datetime')
   
    def starttime_button(self,obj):
        print obj.pk
        return "<a href=\"start_activity/%d\"> fuffa </a>" % obj.pk
    starttime_button.allow_tags = True

    def get_urls(self):
        urls = super(ActivityAdmin, self).get_urls()
        my_urls = patterns('',
        (r'^start_activity/(?P<activity_id>\d+)/$', self.admin_site.admin_view(self.starttime_button_view))
        )
        return my_urls + urls

    def starttime_button_view(self, request, activity_id):
        print activity_id
        activity = get_object_or_404(Activity, pk=activity_id)
        activity.start_datetime = datetime.now()
        activity.save()
        return HttpResponse("Complimenti, hai appena aggiunto lo start_time alla tua activity :3 !!! Lo start_time ora vale:%s\n%s" % (activity.start_datetime,"<a href=\"../..\"> back </a>"))

'''    def get_changelist(self,request):
        user = request.user
        for ch in user.costholder_set.all():
            Activity.objects.get_or_create(costholder=self, user=user, start_datetime__isnull = True)
        return super(ActivityAdmin, self).get_changelist(request)
'''
admin.site.register(CostHolder)
admin.site.register(Activity, ActivityAdmin)

