from django.db import models

class Tech(models.Model):
    type = models.CharField(max_length=50)
    effect_name = models.CharField(max_length=100)
    effect_val = models.DecimalField(max_digits=6, decimal_places=2)

    def __unicode__(self):
        return str({self.type:(self.effect_name,self.effect_val)})
