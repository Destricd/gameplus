from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from .function import *
from .forms import GamesFilterForm
from .forms import ContractsForm


class MainPage(View):
    def get(self, request):
        context = {}
        return render(request, 'main.html', context=context)


class GamesPage(View):
    def get(self, request):
        g_games = get_games()
        form = GamesFilterForm(request.GET)

        if form.is_valid():
            if form.cleaned_data["search"]:
                g_games = g_games.filter(name__iregex=form.cleaned_data["search"])

            if form.cleaned_data["ordering"]:
                g_games = g_games.order_by(form.cleaned_data["ordering"])

        context = {
            'g_games': g_games,
            'form': form
        }
        return render(request, 'games.html', context=context)


class GameOnePage(View):
    def get(self, request, id):
        g_games = get_games()
        game_info = get_gameinfo(id)
        form = GamesFilterForm(request.GET)

        if form.is_valid():
            if form.cleaned_data["search"]:
                g_games = g_games.filter(name__iregex=form.cleaned_data["search"])

            if form.cleaned_data["ordering"]:
                g_games = g_games.order_by(form.cleaned_data["ordering"])

        context = {
            'g_games': g_games,
            'game_info': game_info,
            'form': form
        }
        return render(request, 'games.html', context=context)


class CreateContract(View):
    def get(self, request, id):
        form = ContractsForm()
        form.fields['employee_id'].queryset = (Employee.objects.filter(access_level__in=['A', 'M']))

        context = {
            'form': form
        }
        return render(request, 'newcontract.html', context=context)

    def post(self, request, id):
        form = ContractsForm(request.POST)
        form.fields['employee_id'].queryset = (Employee.objects.filter(access_level__in=['A', 'M']))

        context = {
            'form': form
        }
        if form.is_valid():
            contract = form.save(commit=False)
            contract.game_id = Game.objects.get(id=id)
            contract.save()
            return HttpResponseRedirect('/games.html')
        else:
            context["error"] = "Неправильное заполнение"
            return render(request, 'newcontract.html', context=context)


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


class ReviewsPage(View):
    def get(self, request):
        context = {}
        return render(request, 'reviews.html', context=context)


class SequrityPage(View):
    def get(self, request):
        context = {}
        return render(request, 'sequrity.html', context=context)
