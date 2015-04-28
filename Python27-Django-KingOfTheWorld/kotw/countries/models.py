from django.db import models
from django.contrib.auth.models import User

class Country(models.Model):
    GOVERNMENTS = (
        ('M', 'Monarchy'),
        ('F', 'Facism'),
        ('DI', 'Dictatorship'),
        ('C', 'Communism'),
        ('T', 'Theocracy'),
        ('R', 'Republic'),
        ('DE', 'Democracy'),
    )
    user = models.OneToOneField(User)
    name = models.CharField(max_length=50, unique=True)
    government = models.CharField(max_length=2, choices=GOVERNMENTS, default='M')
    def __unicode__(self):
        return str([self.user,self.name,self.government])

class Build(models.Model):
    country = models.ForeignKey(Country, unique=True)
    unused = models.IntegerField(default=200)
    farm = models.IntegerField(default=40)
    enterprise = models.IntegerField(default=60)
    residence = models.IntegerField(default=100)
    industry = models.IntegerField(default=0)
    army = models.IntegerField(default=0)
    labs = models.IntegerField(default=0)
    oil = models.IntegerField(default=0)
    def __unicode__(self):
        return str({self.country: [self.unused, self.farm, self.enterprise, self.residence, self.industry, self.army, self.labs, self.oil]})

class Army(models.Model):
    country = models.ForeignKey(Country, unique=True)
    troops = models.IntegerField(default=250)
    jets = models.IntegerField(default=0)
    turrets = models.IntegerField(default=0)
    tanks = models.IntegerField(default=0)
    def __unicode__(self):
        return str({self.country: [self.troops, self.jets, self.turrets, self.tanks]})

class Resource(models.Model):
    country = models.ForeignKey(Country, unique=True)
    land = models.IntegerField(default=400)
    gold = models.IntegerField(default=300000)
    food = models.IntegerField(default=50000)
    pop = models.IntegerField(default=10000)
    oil = models.IntegerField(default=0)
    def __unicode__(self):
        return str({self.country: [self.land,self.gold,self.food,self.pop,self.oil]})

class Tech(models.Model):
    country = models.ForeignKey(Country, unique=True)
    military = models.IntegerField(default=100)
    medical = models.IntegerField(default=100)
    economics = models.IntegerField(default=100)
    residential = models.IntegerField(default=100)
    geography = models.IntegerField(default=100)
    weapons = models.IntegerField(default=100)
    def __unicode__(self):
        return str({self.country: [self.military, self.medical, self.economics, self.residential, self.geography, self.weapons]})