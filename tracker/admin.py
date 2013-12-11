from django.contrib import admin
from tracker.models import CostHolder, Goal, Result, Activity, ActivityRecord
from datetime import timedelta


class ActivityRecordAdmin(admin.ModelAdmin):
    list_display = ('activity', 'start_datetime', 'end_datetime', 'delta_seconds', 'notes')
    list_editable = ('start_datetime', 'end_datetime', 'notes')


admin.site.register(CostHolder)
admin.site.register(Goal)
admin.site.register(Result)
admin.site.register(Activity)
admin.site.register(ActivityRecord, ActivityRecordAdmin)

