from django.db import models
import datetime


class Game(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    rate = models.CharField(max_length=10)
    rules = models.TextField(default=' ')
    release_date = models.DateField(default=datetime.now)
    site = models.CharField(max_length=20)
    number_of_rules = models.BooleanField(default=False)
    price = models.DecimalField(decimal_places=2)
    development_budget = models.DecimalField(decimal_places=2)


class GameDevelopmentStages(models.Model):

    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    stage_description = models.TextField(default=' ')


class Employee(models.Model):
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    access_level = models.CharField(max_length=1)
    site = models.CharField(max_length=20)
    number_of_rules = models.BooleanField(default=False)
    price = models.DecimalField(decimal_places=2)
    development_budget = models.DecimalField(decimal_places=2)


class Client(models.Model):
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    rules = models.TextField(default=' ')
    release_date = models.DateField(default=datetime.now)
    site = models.CharField(max_length=20)
    number_of_rules = models.BooleanField(default=False)
    price = models.DecimalField(decimal_places=2)
    development_budget = models.DecimalField(decimal_places=2)