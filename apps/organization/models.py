from django.contrib.auth.models import User
from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='organizations', blank=True)

    def __str__(self):
        return self.name