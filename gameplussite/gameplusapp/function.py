from .models import *


def get_games():
    games = Game.objects.all()
    return games


def get_reviews():
    reviews = Review.objects.all()
    return reviews


def get_accounts():
    accounts = Employee.objects.all()
    return accounts
