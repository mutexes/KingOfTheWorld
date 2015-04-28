from django.db import models

class Building(models.Model):
    type = models.CharField(max_length=50)
    effect_name = models.CharField(max_length=50)
    effect_val = models.DecimalField(max_digits=5, decimal_places=2)
    def __unicode__(self):
        return self.type
