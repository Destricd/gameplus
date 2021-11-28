from django.db import models
from django.utils import timezone


class Game(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    rate = models.CharField(max_length=10)
    rules = models.TextField(default=' ')
    release_date = models.DateField(default=timezone.now())
    site = models.CharField(max_length=63)
    number_of_rules = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    development_budget = models.DecimalField(max_digits=12, decimal_places=2)
    picture = models.ImageField(upload_to="static/images/games", null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class GameDevelopmentStage(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now())
    end_date = models.DateField(default=timezone.now())
    stage_description = models.TextField(default=' ')


class Employee(models.Model):
    MY_CHOICES = (
        ('a', 'Админ'),
        ('m', 'Мастер'),
        ('c', 'Клиент')
    )
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    access_level = models.CharField(max_length=1, choices=MY_CHOICES)
    email = models.CharField(max_length=30)
    login = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    reg_date = models.DateTimeField(default=timezone.now())
    avatar = models.ImageField(upload_to="static/images/users", null=True, blank=True)

    class Meta:
        ordering = ["-reg_date"]

    def __str__(self):
        return self.full_name


class TechnicalTask(models.Model):
    description = models.TextField(default=' ')
    complete = models.BooleanField(default=False)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        ordering = ["employee_id"]


class Review(models.Model):
    client_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    review_text = models.CharField(max_length=200)
    public_date = models.DateTimeField(default=timezone.now())

    class Meta:
        ordering = ["-public_date"]


class ContractOfDevelopment(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    conclusion_date = models.DateField(default=timezone.now())
    contract_end_date = models.DateField(default=timezone.now())
    client_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='client_id')
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_id')
    development_full_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ["game_id"]


class Chat(models.Model):
    members = models.ManyToManyField(Employee)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    letter = models.TextField(default=' ')
    pub_date = models.DateTimeField(default=timezone.now())
    is_readed = models.BooleanField(default=False)

    class Meta:
        ordering = ['pub_date']

