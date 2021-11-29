from .models import *


def autoriz(login, password):
    users = Employee.objects.filter(login=login, password=password)
    return users


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


def get_tasks():
    tasks = TechnicalTask.objects.all()
    return tasks


def get_states():
    states = GameDevelopmentStage.objects.all()
    return states


def get_del_account(pk):
    account = Employee.objects.get(id=pk)
    return account


def get_del_contract(pk):
    contract = ContractOfDevelopment.objects.get(id=pk)
    return contract


def get_del_game(pk):
    game = Game.objects.get(id=pk)
    return game


def get_del_task(pk):
    task = TechnicalTask.objects.get(id=pk)
    return task


def get_del_state(pk):
    state = GameDevelopmentStage.objects.get(id=pk)
    return state


def get_del_review(pk):
    review = Review.objects.get(id=pk)
    return review
