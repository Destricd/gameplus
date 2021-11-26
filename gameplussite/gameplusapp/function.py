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


def get_contracts():
    contracts = ContractOfDevelopment.objects.all()
    return contracts


def get_del_account(pk):
    account = Employee.objects.get(id=pk)
    return account


def get_del_contract(pk):
    contract = ContractOfDevelopment.objects.get(id=pk)
    return contract


def get_del_game(pk):
    game = Game.objects.get(id=pk)
    return game
