from django.db import models

class Government(models.Model):
    type = models.CharField(max_length=50)
    def __unicode__(self):
        return self.type

class effects(models.Model):
    government = models.ForeignKey(Government)
    effect_name = models.CharField(max_length=50)
    effect_val = models.DecimalField(max_digits=6, decimal_places=2)
    def __unicode__(self):
        return str((self.effect_name, self.effect_val))

