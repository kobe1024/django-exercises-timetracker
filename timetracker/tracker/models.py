from django.db import models

from django.contrib.auth.models import User

class CostHolder(models.Model):
    """Represents the cost holder to which all activities are referred.

    Each user perform some kind of activity that is bound to a cost holder,
    which is the object the customer pays for
    """

    name = charfield 256 
    description = text blank
    user_set = manytomany al modello User blank null
    status = charfield 32 choices CREATED, OPEN, CLOSE

    @property
    def delta(self):
        return totale delta activity

    @property
    def delta_for_user(self, user):
        return totale delta activity per utente specifico


class Activity(models.Model):

    cost_holder = foreignkey CostHolder
    user = foreignkey User
    name = char 512 blank
    notes = text blank # not used probably
    start_datetime = datetimefield null blank
    end_datetime = datetimefield null blank

    class Meta:
        ordering = inverso dello start datetime con start = null in alto

    @property
    def delta(self):
        return self.end_datetime - self.start_datetime
    
    
    

