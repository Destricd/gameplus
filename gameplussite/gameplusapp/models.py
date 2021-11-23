from django.db import models
from django.utils import timezone


class Game(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    rate = models.CharField(max_length=10)
    rules = models.TextField(default=' ')
    release_date = models.DateField(default=timezone.now())
    site = models.CharField(max_length=20)
    number_of_rules = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    development_budget = models.DecimalField(max_digits=12, decimal_places=2)
    picture = models.ImageField(upload_to="static/images/games", blank=True)

    class Meta:
        ordering = ["name"]


class GameDevelopmentStage(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now())
    end_date = models.DateField(default=timezone.now())
    stage_description = models.TextField(default=' ')


class Employee(models.Model):
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    access_level = models.CharField(max_length=1)
    email = models.CharField(max_length=30)
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.full_name


class TechnicalTask(models.Model):
    description = models.TextField(default=' ')
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)


class Review(models.Model):
    client_name = models.CharField(max_length=50)
    client_email = models.CharField(max_length=30)
    review_text = models.CharField(max_length=200)


class ContractOfDevelopment(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    conclusion_date = models.DateField(default=timezone.now())
    contract_end_date = models.DateField(default=timezone.now())
    client_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='client_id_a')
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_id_a')
    development_full_price = models.DecimalField(max_digits=12, decimal_places=2)


class Message(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_id_b')
    client_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='client_id_b')
    letter = models.TextField(default=' ')

