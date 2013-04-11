from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField('start')
    end_time = models.DateTimeField('end')
    location = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title
