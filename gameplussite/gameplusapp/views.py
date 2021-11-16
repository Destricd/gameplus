from django.shortcuts import render
from django.views import View
from .function import *


class MainPage(View):
    def get(self, request):
        context = {}
        return render(request, 'main.html', context=context)

    
class GamesPage(View):
    def get(self, request, id):
        g_games = get_games()
        game_info = get_gameinfo(id)
        context = {
            'g_games': g_games,
            'game_info': game_info
        }
        return render(request, 'games.html', context=context)


class AccountPage(View):
    def get(self, request):
        context = {}
        return render(request, 'account.html', context=context)


class AllGamesPage(View):
    def get(self, request):
        context = {}
        return render(request, 'allgames.html', context=context)


class AllTasksPage(View):
    def get(self, request):
        context = {}
        return render(request, 'alltasks.html', context=context)


class ContractsPage(View):
    def get(self, request):
        context = {}
        return render(request, 'contracts.html', context=context)


class ControlPage(View):
    def get(self, request):
        context = {}
        return render(request, 'control.html', context=context)


class LoginPage(View):
    def get(self, request):
        context = {}
        return render(request, 'login.html', context=context)


class MessagesPage(View):
    def get(self, request):
        context = {}
        return render(request, 'messages.html', context=context)


class PrivatesPage(View):
    def get(self, request):
        context = {}
        return render(request, 'privates.html', context=context)


class ReviewsPage(View):
    def get(self, request):
        context = {}
        return render(request, 'reviews.html', context=context)


class SequrityPage(View):
    def get(self, request):
        context = {}
        return render(request, 'sequrity.html', context=context)
