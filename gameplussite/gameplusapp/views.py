import datetime

from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from .function import *
from .forms import GamesFilterForm
from .forms import ContractsForm
from .forms import ReviewsForm
from .forms import ReviewsFilterForm
from .forms import AccountsForm
from .forms import AccountsFilterForm


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
        g_accounts = get_accounts()
        form = AccountsForm()
        filtred = AccountsFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_accounts = g_accounts.filter(full_name__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["ordering"]:
                g_accounts = g_accounts.order_by(filtred.cleaned_data["ordering"])

            if filtred.cleaned_data["watching"]:
                g_accounts = g_accounts.filter(access_level=filtred.cleaned_data["watching"])

        context = {
            'g_accounts': g_accounts,
            'filtred': filtred,
            'form': form
        }
        return render(request, 'control.html', context=context)

    def post(self, request):
        g_accounts = get_accounts()
        form = AccountsForm(request.POST)
        filtred = AccountsFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_accounts = g_accounts.filter(full_name__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["ordering"]:
                g_accounts = g_accounts.order_by(filtred.cleaned_data["ordering"])

            if filtred.cleaned_data["watching"]:
                g_accounts = g_accounts.filter(access_level=filtred.cleaned_data["watching"])

        context = {
            'g_accounts': g_accounts,
            'filtred': filtred,
            'form': form
        }
        if form.is_valid():
            account = form.save(commit=False)
            account.public_date = datetime.datetime.now()
            account.save()
            return HttpResponseRedirect('control.html')
        else:
            context["error"] = "Неправильное заполнение"
            return render(request, 'control.html', context=context)


class ControlOnePage(View):
    def get(self, request, id):
        g_accounts = get_accounts()
        form = AccountsForm(initial={'full_name': g_accounts.get(id=id).full_name,
                                    'login': g_accounts.get(id=id).login,
                                    'password': g_accounts.get(id=id).password})
        filtred = AccountsFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_accounts = g_accounts.filter(full_name__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["ordering"]:
                g_accounts = g_accounts.order_by(filtred.cleaned_data["ordering"])

            if filtred.cleaned_data["watching"]:
                g_accounts = g_accounts.filter(access_level=filtred.cleaned_data["watching"])

        context = {
            'g_accounts': g_accounts,
            'filtred': filtred,
            'form': form
        }
        return render(request, 'control.html', context=context)

    def post(self, request, id):
        g_accounts = get_accounts()
        form = AccountsForm(request.POST)
        filtred = AccountsFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_accounts = g_accounts.filter(full_name__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["ordering"]:
                g_accounts = g_accounts.order_by(filtred.cleaned_data["ordering"])

            if filtred.cleaned_data["watching"]:
                g_accounts = g_accounts.filter(access_level=filtred.cleaned_data["watching"])

        context = {
            'g_accounts': g_accounts,
            'filtred': filtred,
            'form': form
        }
        if form.is_valid():
            account = Employee.objects.get(id=id)
            account.full_name = form.cleaned_data["full_name"]
            account.login = form.cleaned_data["login"]
            account.password = form.cleaned_data["password"]
            account.save()
            return HttpResponseRedirect('/control.html')
        else:
            context["error"] = "Неправильное заполнение"
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
        g_reviews = get_reviews()
        form = ReviewsForm()
        filtred = ReviewsFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_reviews = g_reviews.filter(review_text__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["ordering"]:
                g_reviews = g_reviews.order_by(filtred.cleaned_data["ordering"])

        context = {
            'g_reviews': g_reviews,
            'filtred': filtred,
            'form': form
        }
        return render(request, 'reviews.html', context=context)

    def post(self, request):
        g_reviews = get_reviews()
        form = ReviewsForm(request.POST)
        filtred = ReviewsFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_reviews = g_reviews.filter(review_text__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["ordering"]:
                g_reviews = g_reviews.order_by(filtred.cleaned_data["ordering"])

        context = {
            'g_reviews': g_reviews,
            'filtred': filtred,
            'form': form
        }
        if form.is_valid():
            review = form.save(commit=False)
            review.public_date = datetime.datetime.now()
            review.save()
            return HttpResponseRedirect('reviews.html')
        else:
            context["error"] = "Неправильное заполнение"
            return render(request, 'reviews.html', context=context)


class ReviewOnePage(View):
    def get(self, request, id):
        g_reviews = get_reviews()
        form = ReviewsForm(initial={'review_text': g_reviews.get(id=id).review_text})
        filtred = ReviewsFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_reviews = g_reviews.filter(review_text__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["ordering"]:
                g_reviews = g_reviews.order_by(filtred.cleaned_data["ordering"])

        context = {
            'g_reviews': g_reviews,
            'filtred': filtred,
            'form': form
        }
        return render(request, 'reviews.html', context=context)

    def post(self, request, id):
        g_reviews = get_reviews()
        form = ReviewsForm(request.POST)
        filtred = ReviewsFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_reviews = g_reviews.filter(review_text__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["ordering"]:
                g_reviews = g_reviews.order_by(filtred.cleaned_data["ordering"])

        context = {
            'g_reviews': g_reviews,
            'filtred': filtred,
            'form': form
        }
        if form.is_valid():
            review = Review.objects.get(id=id)
            review.review_text = form.cleaned_data["review_text"]
            review.save()
            return HttpResponseRedirect('/reviews.html')
        else:
            context["error"] = "Неправильное заполнение"
            return render(request, 'reviews.html', context=context)


class SequrityPage(View):
    def get(self, request):
        context = {}
        return render(request, 'sequrity.html', context=context)
