from django.db import models

class Military(models.Model):
    unit = models.CharField(max_length=50)
    offense = models.IntegerField()
    defense = models.IntegerField()
    fuel = models.IntegerField()
    def __unicode__(self):
        return self.unit
