from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):

    STATUS_CHOICES = [
        ('Done', 'completed'),
        ('Not Done', 'not completed')
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES, default="Not Done")


    def __str__(self):
        return self.title