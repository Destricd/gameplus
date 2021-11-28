import datetime

from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from .function import *
from .forms import GamesForm
from .forms import GamesFilterForm
from .forms import ContractsForm
from .forms import ReviewsForm
from .forms import ReviewsFilterForm
from .forms import AccountsForm
from .forms import AccountsFilterForm
from .forms import ContractsInfoForm
from .forms import ContractsFilterForm
from .forms import TasksForm
from .forms import TasksFilterForm


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
        game_info = Game.objects.get(id=id)
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
        form.fields['employee_id'].queryset = (Employee.objects.filter(access_level__in=['a', 'm']))

        context = {
            'form': form
        }
        return render(request, 'newcontract.html', context=context)

    def post(self, request, id):
        form = ContractsForm(request.POST)
        form.fields['employee_id'].queryset = (Employee.objects.filter(access_level__in=['a', 'm']))

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
        mod = "добавление"
        g_games = get_games()
        form = GamesForm()
        filtred = GamesFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_games = g_games.filter(name__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["ordering"]:
                g_games = g_games.order_by(filtred.cleaned_data["ordering"])

        context = {
            'g_games': g_games,
            'filtred': filtred,
            'form': form,
            'mod': mod
        }
        return render(request, 'allgames.html', context=context)

    def post(self, request):
        mod = "добавление"
        g_games = get_games()
        form = GamesForm(request.POST)
        filtred = GamesFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_games = g_games.filter(name__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["ordering"]:
                g_games = g_games.order_by(filtred.cleaned_data["ordering"])

        context = {
            'g_games': g_games,
            'filtred': filtred,
            'form': form,
            'mod': mod
        }
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('allgames.html')
        else:
            context["error"] = "Неправильное заполнение"
            return render(request, 'allgames.html', context=context)


class GameListOnePage(View):
    def get(self, request, id):
        mod = "редактирование"
        game_id = id
        g_games = get_games()
        picture = g_games.get(id=id).picture
        form = GamesForm(initial={'name': g_games.get(id=id).name,
                                  'type': g_games.get(id=id).type,
                                  'rate': g_games.get(id=id).rate,
                                  'rules': g_games.get(id=id).rules,
                                  'release_date': g_games.get(id=id).release_date,
                                  'site': g_games.get(id=id).site,
                                  'number_of_rules': g_games.get(id=id).number_of_rules,
                                  'price': g_games.get(id=id).price,
                                  'development_budget': g_games.get(id=id).development_budget,
                                  'picture': g_games.get(id=id).picture
                                  })
        filtred = GamesFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_games = g_games.filter(name__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["ordering"]:
                g_games = g_games.order_by(filtred.cleaned_data["ordering"])

        context = {
            'g_games': g_games,
            'filtred': filtred,
            'form': form,
            'mod': mod,
            'picture': picture,
            'game_id': game_id
        }
        return render(request, 'allgames.html', context=context)

    def post(self, request, id):
        mod = "редактирование"
        game_id = id
        g_games = get_games()
        picture = g_games.get(id=id).picture
        form = GamesForm(request.POST, request.FILES)
        filtred = GamesFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_games = g_games.filter(name__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["ordering"]:
                g_games = g_games.order_by(filtred.cleaned_data["ordering"])

        context = {
            'g_games': g_games,
            'filtred': filtred,
            'form': form,
            'mod': mod,
            'picture': picture,
            'game_id': game_id
        }
        if form.is_valid():
            game = Game.objects.get(id=id)
            game.name = form.cleaned_data["name"]
            game.type = form.cleaned_data["type"]
            game.rate = form.cleaned_data["rate"]
            game.rules = form.cleaned_data["rules"]
            game.release_date = form.cleaned_data["release_date"]
            game.site = form.cleaned_data["site"]
            game.number_of_rules = form.cleaned_data["number_of_rules"]
            game.price = form.cleaned_data["price"]
            game.development_budget = form.cleaned_data["development_budget"]
            if form.cleaned_data["picture"] != None:
                game.picture = form.cleaned_data["picture"]
            game.save()
            return HttpResponseRedirect('/allgames.html')
        else:
            context["error"] = "Неправильное заполнение"
            return render(request, 'allgames.html', context=context)


class AllTasksPage(View):
    def get(self, request):
        mod = "добавление"
        g_tasks = get_tasks()
        form = TasksForm()
        form.fields['employee_id'].queryset = (Employee.objects.filter(access_level='m'))
        filtred = TasksFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_tasks = g_tasks.filter(employee_id__full_name__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["watching"]:
                if filtred.cleaned_data["watching"] == "a":
                    g_tasks = g_tasks.filter(complete=True)
                elif filtred.cleaned_data["watching"] == "b":
                    g_tasks = g_tasks.filter(complete=False)

        context = {
            'g_tasks': g_tasks,
            'filtred': filtred,
            'form': form,
            'mod': mod
        }
        return render(request, 'alltasks.html', context=context)

    def post(self, request):
        mod = "добавление"
        g_tasks = get_tasks()
        form = TasksForm(request.POST)
        form.fields['employee_id'].queryset = (Employee.objects.filter(access_level='m'))
        filtred = TasksFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_tasks = g_tasks.filter(employee_id__full_name__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["watching"]:
                if filtred.cleaned_data["watching"] == "a":
                    g_tasks = g_tasks.filter(complete=True)
                elif filtred.cleaned_data["watching"] == "b":
                    g_tasks = g_tasks.filter(complete=False)

        context = {
            'g_tasks': g_tasks,
            'filtred': filtred,
            'form': form,
            'mod': mod
        }
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('alltasks.html')
        else:
            context["error"] = "Неправильное заполнение"
            return render(request, 'alltasks.html', context=context)


class TaskOnePage(View):
    def get(self, request, id):
        mod = "редактирование"
        task_id = id
        g_tasks = get_tasks()
        form = TasksForm(initial={'employee_id': g_tasks.get(id=id).employee_id,
                                  'description': g_tasks.get(id=id).description,
                                  'complete': g_tasks.get(id=id).complete})
        form.fields['employee_id'].queryset = (Employee.objects.filter(access_level='m'))
        filtred = TasksFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_tasks = g_tasks.filter(employee_id__full_name__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["watching"]:
                if filtred.cleaned_data["watching"] == "a":
                    g_tasks = g_tasks.filter(complete=True)
                elif filtred.cleaned_data["watching"] == "b":
                    g_tasks = g_tasks.filter(complete=False)

        context = {
            'g_tasks': g_tasks,
            'filtred': filtred,
            'form': form,
            'mod': mod,
            'task_id': task_id
        }
        return render(request, 'alltasks.html', context=context)

    def post(self, request, id):
        mod = "редактирование"
        task_id = id
        g_tasks = get_tasks()
        form = TasksForm(request.POST)
        form.fields['employee_id'].queryset = (Employee.objects.filter(access_level='m'))
        filtred = TasksFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_tasks = g_tasks.filter(employee_id__full_name__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["watching"]:
                if filtred.cleaned_data["watching"] == "a":
                    g_tasks = g_tasks.filter(complete=True)
                elif filtred.cleaned_data["watching"] == "b":
                    g_tasks = g_tasks.filter(complete=False)

        context = {
            'g_tasks': g_tasks,
            'filtred': filtred,
            'form': form,
            'mod': mod,
            'task_id': task_id
        }
        if form.is_valid():
            task = TechnicalTask.objects.get(id=id)
            task.employee_id = form.cleaned_data["employee_id"]
            task.description = form.cleaned_data["description"]
            task.complete = form.cleaned_data["complete"]
            task.save()
            return HttpResponseRedirect('/alltasks.html')
        else:
            context["error"] = "Неправильное заполнение"
            return render(request, 'alltasks.html', context=context)


class ContractsPage(View):
    def get(self, request):
        mod = "добавление"
        g_contracts = get_contracts()
        form = ContractsInfoForm()
        form.fields['employee_id'].queryset = (Employee.objects.filter(access_level__in=['a', 'm']))
        filtred = ContractsFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_contracts = g_contracts.filter(game_id__name__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["ordering"]:
                g_contracts = g_contracts.order_by(filtred.cleaned_data["ordering"])

            if filtred.cleaned_data["watching"]:
                if filtred.cleaned_data["watching"] == "a":
                    g_contracts = g_contracts.filter(conclusion_date__gt=datetime.datetime.now())
                elif filtred.cleaned_data["watching"] == "b":
                    g_contracts = g_contracts.filter(conclusion_date__lt=datetime.datetime.now(),
                                                     contract_end_date__gt=datetime.datetime.now())
                elif filtred.cleaned_data["watching"] == "c":
                    g_contracts = g_contracts.filter(contract_end_date__lt=datetime.datetime.now())

        context = {
            'g_contracts': g_contracts,
            'filtred': filtred,
            'form': form,
            'mod': mod
        }
        return render(request, 'contracts.html', context=context)

    def post(self, request):
        mod = "добавление"
        g_contracts = get_contracts()
        form = ContractsInfoForm(request.POST)
        form.fields['employee_id'].queryset = (Employee.objects.filter(access_level__in=['a', 'm']))
        filtred = ContractsFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_contracts = g_contracts.filter(game_id__name__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["ordering"]:
                g_contracts = g_contracts.order_by(filtred.cleaned_data["ordering"])

            if filtred.cleaned_data["watching"]:
                if filtred.cleaned_data["watching"] == "a":
                    g_contracts = g_contracts.filter(conclusion_date__gt=datetime.datetime.now())
                elif filtred.cleaned_data["watching"] == "b":
                    g_contracts = g_contracts.filter(conclusion_date__lt=datetime.datetime.now(),
                                                     contract_end_date__gt=datetime.datetime.now())
                elif filtred.cleaned_data["watching"] == "c":
                    g_contracts = g_contracts.filter(contract_end_date__lt=datetime.datetime.now())

        context = {
            'g_contracts': g_contracts,
            'filtred': filtred,
            'form': form,
            'mod': mod
        }
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('contracts.html')
        else:
            context["error"] = "Неправильное заполнение"
            return render(request, 'contracts.html', context=context)


class ContractOnePage(View):
    def get(self, request, id):
        mod = "редактирование"
        note_id = id
        g_contracts = get_contracts()
        form = ContractsInfoForm(initial={'game_id': g_contracts.get(id=id).game_id,
                                          'conclusion_date': g_contracts.get(id=id).conclusion_date,
                                          'contract_end_date': g_contracts.get(id=id).contract_end_date,
                                          'client_id': g_contracts.get(id=id).client_id,
                                          'employee_id': g_contracts.get(id=id).employee_id,
                                          'development_full_price': g_contracts.get(id=id).development_full_price})
        form.fields['employee_id'].queryset = (Employee.objects.filter(access_level__in=['a', 'm']))
        filtred = ContractsFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_contracts = g_contracts.filter(game_id__name__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["ordering"]:
                g_contracts = g_contracts.order_by(filtred.cleaned_data["ordering"])

            if filtred.cleaned_data["watching"]:
                if filtred.cleaned_data["watching"] == "a":
                    g_contracts = g_contracts.filter(conclusion_date__gt=datetime.datetime.now())
                elif filtred.cleaned_data["watching"] == "b":
                    g_contracts = g_contracts.filter(conclusion_date__lt=datetime.datetime.now(),
                                                     contract_end_date__gt=datetime.datetime.now())
                elif filtred.cleaned_data["watching"] == "c":
                    g_contracts = g_contracts.filter(contract_end_date__lt=datetime.datetime.now())

        context = {
            'g_contracts': g_contracts,
            'filtred': filtred,
            'form': form,
            'mod': mod,
            'note_id': note_id
        }
        return render(request, 'contracts.html', context=context)

    def post(self, request, id):
        mod = "редактирование"
        note_id = id
        g_contracts = get_contracts()
        form = ContractsInfoForm(request.POST)
        form.fields['employee_id'].queryset = (Employee.objects.filter(access_level__in=['a', 'm']))
        filtred = ContractsFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_contracts = g_contracts.filter(game_id__name__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["ordering"]:
                g_contracts = g_contracts.order_by(filtred.cleaned_data["ordering"])

            if filtred.cleaned_data["watching"]:
                if filtred.cleaned_data["watching"] == "a":
                    g_contracts = g_contracts.filter(conclusion_date__gt=datetime.datetime.now())
                elif filtred.cleaned_data["watching"] == "b":
                    g_contracts = g_contracts.filter(conclusion_date__lt=datetime.datetime.now(),
                                                     contract_end_date__gt=datetime.datetime.now())
                elif filtred.cleaned_data["watching"] == "c":
                    g_contracts = g_contracts.filter(contract_end_date__lt=datetime.datetime.now())

        context = {
            'g_contracts': g_contracts,
            'filtred': filtred,
            'form': form,
            'mod': mod,
            'note_id': note_id
        }
        if form.is_valid():
            contract = ContractOfDevelopment.objects.get(id=id)
            contract.game_id = form.cleaned_data["game_id"]
            contract.conclusion_date = form.cleaned_data["conclusion_date"]
            contract.contract_end_date = form.cleaned_data["contract_end_date"]
            contract.client_id = form.cleaned_data["client_id"]
            contract.employee_id = form.cleaned_data["employee_id"]
            contract.development_full_price = form.cleaned_data["development_full_price"]
            contract.save()
            return HttpResponseRedirect('/contracts.html')
        else:
            context["error"] = "Неправильное заполнение"
            return render(request, 'contracts.html', context=context)


class ControlPage(View):
    def get(self, request):
        mod = "добавление"
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
            'form': form,
            'mod': mod
        }
        return render(request, 'control.html', context=context)

    def post(self, request):
        mod = "добавление"
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
            'form': form,
            'mod': mod
        }
        if form.is_valid():
            account = form.save(commit=False)
            account.reg_date = datetime.datetime.now()
            account.save()
            return HttpResponseRedirect('control.html')
        else:
            context["error"] = "Неправильное заполнение"
            return render(request, 'control.html', context=context)


class ControlOnePage(View):
    def get(self, request, id):
        mod = "редактирование"
        user_id = id
        g_accounts = get_accounts()
        avatar = g_accounts.get(id=id).avatar
        form = AccountsForm(initial={'full_name': g_accounts.get(id=id).full_name,
                                     'password': g_accounts.get(id=id).password,
                                     'phone': g_accounts.get(id=id).phone,
                                     'email': g_accounts.get(id=id).email,
                                     'access_level': g_accounts.get(id=id).access_level,
                                     'avatar': g_accounts.get(id=id).avatar})
        form.fields["login"].required = False
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
            'form': form,
            'mod': mod,
            'avatar': avatar,
            'user_id': user_id
        }
        return render(request, 'control.html', context=context)

    def post(self, request, id):
        mod = "редактирование"
        user_id = id
        g_accounts = get_accounts()
        avatar = g_accounts.get(id=id).avatar
        form = AccountsForm(request.POST, request.FILES)
        form.fields["login"].required = False
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
            'form': form,
            'mod': mod,
            'avatar': avatar,
            'user_id': user_id
        }
        if form.is_valid():
            account = Employee.objects.get(id=id)
            account.full_name = form.cleaned_data["full_name"]
            if form.cleaned_data["login"] != '':
                account.login = form.cleaned_data["login"]
            account.password = form.cleaned_data["password"]
            account.phone = form.cleaned_data["phone"]
            account.email = form.cleaned_data["email"]
            account.access_level = form.cleaned_data["access_level"]
            if form.cleaned_data["avatar"] != None:
                account.avatar = form.cleaned_data["avatar"]
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
        mod = "Оставить"
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
            'form': form,
            'mod': mod
        }
        return render(request, 'reviews.html', context=context)

    def post(self, request):
        mod = "Оставить"
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
            'form': form,
            'mod': mod
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
        mod = "Редактировать"
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
            'form': form,
            'mod': mod
        }
        return render(request, 'reviews.html', context=context)

    def post(self, request, id):
        mod = "Редактировать"
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
            'form': form,
            'mod': mod
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


class AccountDeletePage(View):
    def get(self, request, id):
        context = {}
        return render(request, 'confirm_delete.html', context=context)

    def post(self, request, id):
        g_del_account = get_del_account(id)
        context = {}
        g_del_account.delete()
        return HttpResponseRedirect('/control.html')


class ContractDeletePage(View):
    def get(self, request, id):
        context = {}
        return render(request, 'confirm_delete.html', context=context)

    def post(self, request, id):
        g_del_contract = get_del_contract(id)
        context = {}
        g_del_contract.delete()
        return HttpResponseRedirect('/contracts.html')


class GameDeletePage(View):
    def get(self, request, id):
        context = {}
        return render(request, 'confirm_delete.html', context=context)

    def post(self, request, id):
        g_del_game = get_del_game(id)
        context = {}
        g_del_game.delete()
        return HttpResponseRedirect('/allgames.html')


class TaskDeletePage(View):
    def get(self, request, id):
        context = {}
        return render(request, 'confirm_delete.html', context=context)

    def post(self, request, id):
        g_del_task = get_del_task(id)
        context = {}
        g_del_task.delete()
        return HttpResponseRedirect('/alltasks.html')
