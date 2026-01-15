from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    GOAL = [('M', 'Maintain'), ('C', 'Cut'), ('B', 'Bulk')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.PositiveSmallIntegerField(help_text='cm')
    weight = models.FloatField(help_text='kg')
    waist = models.PositiveSmallIntegerField(help_text='cm')
    disease = models.CharField(max_length=120, blank=True)
    goal = models.CharField(max_length=1, choices=GOAL, default='M')

    def __str__(self):
        return self.user.username