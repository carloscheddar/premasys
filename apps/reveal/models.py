from django.db import models
from registration.models import User


class Lesson(models.Model):
    username = models.ForeignKey(User, null=True, blank=True)
    slide = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.username
