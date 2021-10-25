from .models import *


def get_games():
    games = Game.objects.all()
    return games


