# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
import json
from datetime import datetime

from tracker.models import User, CostHolder, Activity


def get_users(request):
    """Return list of all users"""

    users_list = User.objects.all().values(
        'id', 'username', 'first_name', 'last_name'
    )

    return HttpResponse(json.dumps(
        {'users': list(users_list)}
    ))


def get_activities_by_user(request, user_id):
    """Return activities related a user in a destructured way"""

    activities_info = []

    for activity in Activity.objects.filter(user=user_id):

        result = activity.result
        goal = result.goal
        ch = goal.cost_holder

        for record in activity.activityrecord_set.all():

            activities_info.append({
                'ch': ch.name,
                'goal': goal.name,
                'result': result.name,
                'activity': activity.name,
                'start': record.start_datetime.isoformat(),
                'end': record.end_datetime.isoformat(),
                'delta': record.delta_seconds,
            })

    return HttpResponse(json.dumps(
        {'activities': activities_info}
    ))


def get_delta_by_ch(request, ch_id):
    """Return total delta related a Cost Holder"""

    ch = CostHolder.objects.get(id=ch_id)
    delta = ch.delta.total_seconds()

    return HttpResponse(
        "<strong>%s</strong> - %s (total delta in seconds)" % (ch, delta)
    )

