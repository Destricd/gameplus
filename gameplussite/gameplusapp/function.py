from .models import *


def get_games():
    games = Game.objects.all()
    return games


def get_gameinfo(id_game):
    gameinformations = Game.objects.filter(id=id_game)
    return gameinformations


def get_reviews():
    reviews = Review.objects.all()
    return reviews
