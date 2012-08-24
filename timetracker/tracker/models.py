from django.db import models

from django.contrib.auth.models import User

import datetime

class CostHolder(models.Model):
    """Represents the cost holder to which all activities are referred.

    Each user perform some kind of activity that is bound to a cost holder,
    which is the object the customer pays for
    """

    STATUS_CHOICES = (
        ('CREATED', 'Created'),
        ('OPEN', 'Open'),
        ('CLOSE', 'Close')
    )

    name = models.CharField(max_length=256) 
    description = models.TextField(blank=True)
   #WAS:  user_set = models.ManyToManyField(User, related_name='u+', blank=True, null=True)
    user_set = models.ManyToManyField(User, blank=True, null=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)

    def create_activities(self):
        for user in self.user_set.all():
            Activity.objects.get_or_create(cost_holder=self, user=user)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kw):
        super(CostHolder, self).save(*args, **kw)
        self.create_activities()

    @property
    def delta(self):
        activities = self.activity_set.all()
        
        return self.__delta_for_activities(activities) #totale delta activity

    def delta_for_user(self, user):
        activities = self.activity_set.filter(user=user)
        
        return self.__delta_for_activities(activities) #totale delta activity per utente specifico

    def __delta_for_activities(self,activities):
        counter = datetime.timedelta(0)
        for activity in activities:
            counter = counter + activity.delta
        
        return counter


class Activity(models.Model):

    cost_holder = models.ForeignKey(CostHolder)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=512,blank=True)
    notes = models.TextField(blank=True) # not used probably
    start_datetime = models.DateTimeField(null=True,blank=True)
    end_datetime = models.DateTimeField(null=True,blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        ordering = ['-start_datetime'] #inverso dello start datetime con start = null in alto

    @property
    def delta(self):
        return self.end_datetime - self.start_datetime #return a timedelta
    
