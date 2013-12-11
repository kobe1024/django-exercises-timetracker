# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from datetime import datetime, timedelta


STATUS_CHOICES = (
    ('CREATED', u"Creato"),
    ('OPEN', u"Aperto"),
    ('CLOSE', u"Chiuso"),
)


class CostHolder(models.Model):
    """Represents the cost holder to which all activities are referred.

    Each user perform some kind of activity that is bound to a cost holder,
    which is the object the customer pays for

    e.g. research&development, sales&marketing
    """

    name = models.CharField(max_length=256)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='CREATED')
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    user_set = models.ManyToManyField(User, blank=True, null=True)

    def __unicode__(self):
        return self.name

    @property
    def delta(self):
        return sum(
            [goal.delta for goal in self.goal_set.all()],
            timedelta(0)
        )

    @property
    def delta_for_user(self, user):
        return sum(
            [goal.delta_for_user(user) for goal in self.goal_set.all()],
            timedelta(0)
        )

    class Meta:
        verbose_name = u"centro di costo"
        verbose_name_plural = u"centri di costo"


class Goal(models.Model):
    """A goal to reach

    e.g. take a client
    """

    cost_holder = models.ForeignKey(CostHolder)
    name = models.CharField(max_length=256)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='CREATED')
    foreseen_end_datetime = models.DateTimeField(null=True, blank=True)
    foreseen_delta = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    @property
    def delta(self):
        return sum(
            [result.delta for result in self.result_set.all()],
            timedelta(0)
        )

    @property
    def delta_for_user(self, user):
        return sum(
            [result.delta_for_user(user) for result in self.result_set.all()],
            timedelta(0)
        )

    class Meta:
        ordering = ['foreseen_end_datetime']
        verbose_name = u"obiettivo"
        verbose_name_plural = u"obiettivi"


class Result(models.Model):
    """Several results in order to reach a goal

    e.g. doing a flavour to that client
    """

    goal = models.ForeignKey(Goal)
    name = models.CharField(max_length=256)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='CREATED')
    foreseen_end_datetime = models.DateTimeField(null=True, blank=True)
    foreseen_delta = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    @property
    def delta(self):
        return sum(
            [activity.delta for activity in self.activity_set.all()],
            timedelta(0)
        )

    @property
    def delta_for_user(self, user):
        return sum(
            [activity.delta for activity in self.activity_set.filter(user=user)],
            timedelta(0)
        )

    class Meta:
        ordering = ['foreseen_end_datetime']
        verbose_name = u"risultato concreto"
        verbose_name_plural = u"risultati concreti"


class Activity(models.Model):
    """An activity which is related an user

    e.g. a user fixes that bug
    """

    result = models.ForeignKey(Result)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=512, blank=True)
    foreseen_end_datetime = models.DateTimeField(null=True, blank=True)
    foreseen_delta = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.user)

    @property
    def delta(self):
        return sum(
            [record.delta for record in self.activityrecord_set.all()],
            timedelta(0)
        )

    class Meta:
        ordering = ['foreseen_end_datetime']
        verbose_name = u"attivita'"
        verbose_name_plural = u"attivita'"

    def save(self, *args, **kwargs):
        # aggiungi un activity record
        super(Activity, self).save(*args, **kwargs)


class ActivityRecord(models.Model):
    """A single session about an activity

    e.g. bugfixing from 3pm to 5pm
    """

    activity = models.ForeignKey(Activity)
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    delta_seconds = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return "%s - %s (%s)" % (self.start_datetime, self.end_datetime, self.activity)

    @property
    def delta(self):
        try:
            delta = timedelta(seconds=self.delta_seconds)
            return delta
        except:
            return timedelta(0)

    class Meta:
        ordering = ['-start_datetime']
        verbose_name = u"singola attivita'"
        verbose_name_plural = u"singole attivita'"

    def save(self, *args, **kwargs):
        """
        if not self.start_datetime:
            return

        if self.end_datetime and self.start_datetime < self.end_datetime:
            delta = self.end_datetime - self.start_datetime
            self.delta_seconds = delta.total_seconds()

        elif self.delta_seconds and self.delta_seconds > 0:
            delta = timedelta(seconds=self.delta_seconds)
            self.end_datetime = self.start_datetime + delta

        else:
            return
        """

        if self.start_datetime:

            if self.end_datetime and self.start_datetime < self.end_datetime:
                delta = self.end_datetime - self.start_datetime
                self.delta_seconds = delta.total_seconds()

            elif self.delta_seconds and self.delta_seconds > 0:
                delta = timedelta(seconds=self.delta_seconds)
                self.end_datetime = self.start_datetime + delta

        super(ActivityRecord, self).save(*args, **kwargs)

        # aggiungi un altro record

