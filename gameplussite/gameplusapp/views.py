import datetime

from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q, Count
from .function import *
from .forms import *


class MainPage(View):
    def get(self, request):
        if "id_user" in request.session:
            link = "confirm_exit.html"
            log = "Выйти"
        else:
            link = "login.html"
            log = "Войти\Регистрация"
        context = {
            'link': link,
            'log': log
        }
        return render(request, 'main.html', context=context)


class GamesPage(View):
    def get(self, request):
        if "id_user" in request.session:
            link = "confirm_exit.html"
            log = "Выйти"
        else:
            link = "login.html"
            log = "Войти\Регистрация"
        g_games = get_games()
        form = GamesFilterForm(request.GET)

        if form.is_valid():
            if form.cleaned_data["search"]:
                g_games = g_games.filter(name__iregex=form.cleaned_data["search"])

            if form.cleaned_data["ordering"]:
                g_games = g_games.order_by(form.cleaned_data["ordering"])

        context = {
            'g_games': g_games,
            'form': form,
            'link': link,
            'log': log
        }
        return render(request, 'games.html', context=context)


class GameOnePage(View):
    def get(self, request, id):
        if "id_user" in request.session:
            link = "confirm_exit.html"
            log = "Выйти"
        else:
            link = "login.html"
            log = "Войти\Регистрация"
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
            'form': form,
            'link': link,
            'log': log,
            'enable': 'enable'
        }
        return render(request, 'games.html', context=context)


class CreateContract(View):
    def get(self, request, id):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        form = ContractsForm()
        form.fields['employee_id'].queryset = (Employee.objects.filter(access_level__in=['a', 'm']))

        context = {
            'form': form
        }
        return render(request, 'newcontract.html', context=context)

    def post(self, request, id):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        form = ContractsForm(request.POST)
        form.fields['employee_id'].queryset = (Employee.objects.filter(access_level__in=['a', 'm']))

        context = {
            'form': form
        }
        if form.is_valid():
            contract = form.save(commit=False)
            contract.game_id = Game.objects.get(id=id)
            contract.client_id = Employee.objects.get(id=request.session["id_user"])
            contract.save()
            return HttpResponseRedirect('/games.html')
        else:
            context["error"] = "Неправильное заполнение"
            return render(request, 'newcontract.html', context=context)


class AccountPage(View):
    def get(self, request):
        if "id_user" not in request.session:
            return HttpResponseRedirect('login.html')
        g_accounts = get_accounts()
        avatar = g_accounts.get(id=request.session["id_user"]).avatar
        form = UserForm(initial={'full_name': g_accounts.get(id=request.session["id_user"]).full_name,
                                 'avatar': g_accounts.get(id=request.session["id_user"]).avatar})
        form.fields["login"].required = False
        context = {
            'form': form,
            'avatar': avatar
        }
        return render(request, 'account.html', context=context)

    def post(self, request):
        if "id_user" not in request.session:
            return HttpResponseRedirect('login.html')
        g_accounts = get_accounts()
        avatar = g_accounts.get(id=request.session["id_user"]).avatar
        form = UserForm(request.POST)
        form.fields["login"].required = False
        context = {
            'form': form,
            'avatar': avatar
        }
        if form.is_valid():
            user = Employee.objects.get(id=request.session["id_user"])
            user.full_name = form.cleaned_data["full_name"]
            if form.cleaned_data["login"] != '':
                user.login = form.cleaned_data["login"]
            user.avatar = form.cleaned_data["avatar"]
            user.save()
            return HttpResponseRedirect('account.html')
        else:
            context["error"] = "Неправильное заполнение"
            return render(request, 'account.html', context=context)


class AllGamesPage(View):
    def get(self, request):
        if "id_user" not in request.session:
            return HttpResponseRedirect('login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            return HttpResponseRedirect('contracts.html')
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
        if "id_user" not in request.session:
            return HttpResponseRedirect('login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            return HttpResponseRedirect('contracts.html')
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
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            return HttpResponseRedirect('/contracts.html')
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
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            return HttpResponseRedirect('/contracts.html')
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
        new = False
        g_tasks = get_tasks()
        if "id_user" not in request.session:
            return HttpResponseRedirect('login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            return HttpResponseRedirect('contracts.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'a':
            new = True
        else:
            g_tasks = g_tasks.filter(employee_id=Employee.objects.get(id=request.session["id_user"]))
        mod = "добавление"
        form = TasksForm()
        form.fields['employee_id'].queryset = (Employee.objects.filter(access_level='m'))
        filtred = TasksFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_tasks = g_tasks.filter(description__iregex=filtred.cleaned_data["search"])

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
            'new': new
        }
        return render(request, 'alltasks.html', context=context)

    def post(self, request):
        new = False
        g_tasks = get_tasks()
        if "id_user" not in request.session:
            return HttpResponseRedirect('login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            return HttpResponseRedirect('contracts.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'a':
            new = True
        else:
            g_tasks = g_tasks.filter(employee_id=Employee.objects.get(id=request.session["id_user"]))
        mod = "добавление"
        form = TasksForm(request.POST)
        form.fields['employee_id'].queryset = (Employee.objects.filter(access_level='m'))
        filtred = TasksFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_tasks = g_tasks.filter(description__iregex=filtred.cleaned_data["search"])

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
            'new': new
        }
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('alltasks.html')
        else:
            context["error"] = "Неправильное заполнение"
            return render(request, 'alltasks.html', context=context)


class TaskOnePage(View):
    def get(self, request, id):
        g_tasks = get_tasks()
        new = True
        form = TasksForm(initial={'employee_id': g_tasks.get(id=id).employee_id,
                                  'description': g_tasks.get(id=id).description,
                                  'complete': g_tasks.get(id=id).complete})
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            return HttpResponseRedirect('/contracts.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'm':
            if TechnicalTask.objects.get(id=id).employee_id != Employee.objects.get(id=request.session["id_user"]):
                return HttpResponseRedirect('/alltasks.html')
            g_tasks = g_tasks.filter(employee_id=Employee.objects.get(id=request.session["id_user"]))
            form.fields["employee_id"].required = False
            form.fields["description"].required = False
            new = False
        mod = "редактирование"
        task_id = id
        form.fields['employee_id'].queryset = (Employee.objects.filter(access_level='m'))
        filtred = TasksFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_tasks = g_tasks.filter(description__iregex=filtred.cleaned_data["search"])

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
            'task_id': task_id,
            'new': new
        }
        return render(request, 'alltasks.html', context=context)

    def post(self, request, id):
        g_tasks = get_tasks()
        new = True
        form = TasksForm(request.POST)
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            return HttpResponseRedirect('/contracts.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'm':
            if TechnicalTask.objects.get(id=id).employee_id != Employee.objects.get(id=request.session["id_user"]):
                return HttpResponseRedirect('/alltasks.html')
            g_tasks = g_tasks.filter(employee_id=Employee.objects.get(id=request.session["id_user"]))
            form.fields["employee_id"].required = False
            form.fields["description"].required = False
            new = False
        mod = "редактирование"
        task_id = id
        form.fields['employee_id'].queryset = (Employee.objects.filter(access_level='m'))
        filtred = TasksFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_tasks = g_tasks.filter(description__iregex=filtred.cleaned_data["search"])

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
            'task_id': task_id,
            'new': new
        }
        if form.is_valid():
            task = TechnicalTask.objects.get(id=id)
            if Employee.objects.get(id=request.session["id_user"]).access_level == 'a':
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
        new = 2
        message = ''
        g_contracts = get_contracts()
        form = ContractsInfoForm()
        if "id_user" not in request.session:
            return HttpResponseRedirect('login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level in ['m', 'c']:
            new = 1
            if Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
                new = 0
            g_contracts = g_contracts.filter(Q(client_id=Employee.objects.get(id=request.session["id_user"])) | Q(
                employee_id=Employee.objects.get(id=request.session["id_user"])))
            form.fields["employee_id"].required = False
        if "message" in request.session:
            if request.session["message"] == True:
                message = 'Доступ запрещён'
                request.session["message"] = False
        mod = "добавление"
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
            'new': new,
            'message': message
        }
        return render(request, 'contracts.html', context=context)

    def post(self, request):
        new = 2
        message = ''
        g_contracts = get_contracts()
        form = ContractsInfoForm(request.POST)
        if "id_user" not in request.session:
            return HttpResponseRedirect('login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level in ['m', 'c']:
            new = 1
            if Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
                new = 0
            g_contracts = g_contracts.filter(Q(client_id=Employee.objects.get(id=request.session["id_user"])) | Q(
                employee_id=Employee.objects.get(id=request.session["id_user"])))
            form.fields["employee_id"].required = False
        if "message" in request.session:
            if request.session["message"] == True:
                message = 'Доступ запрещён'
                request.session["message"] = False
        mod = "добавление"
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
            'new': new,
            'message': message
        }
        if form.is_valid():
            contract = form.save(commit=False)
            if Employee.objects.get(id=request.session["id_user"]).access_level == 'm':
                contract.employee_id = Employee.objects.get(id=request.session["id_user"])
            contract.save()
            return HttpResponseRedirect('contracts.html')
        else:
            context["error"] = "Неправильное заполнение"
            return render(request, 'contracts.html', context=context)


class ContractOnePage(View):
    def get(self, request, id):
        new = 2
        g_contracts = get_contracts()
        form = ContractsInfoForm(initial={'game_id': g_contracts.get(id=id).game_id,
                                          'conclusion_date': g_contracts.get(id=id).conclusion_date,
                                          'contract_end_date': g_contracts.get(id=id).contract_end_date,
                                          'client_id': g_contracts.get(id=id).client_id,
                                          'employee_id': g_contracts.get(id=id).employee_id,
                                          'development_full_price': g_contracts.get(id=id).development_full_price})
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level in ['m', 'c']:
            new = 1
            g_contracts = g_contracts.filter(Q(client_id=Employee.objects.get(id=request.session["id_user"])) | Q(
                employee_id=Employee.objects.get(id=request.session["id_user"])))
            if Employee.objects.get(
                    id=request.session["id_user"]).access_level == 'c' or ContractOfDevelopment.objects.get(
                    id=id) not in g_contracts.filter(employee_id=Employee.objects.get(id=request.session["id_user"])):
                request.session["message"] = True
                return HttpResponseRedirect('/contracts.html')
            form.fields["employee_id"].required = False
        mod = "редактирование"
        note_id = id
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
            'note_id': note_id,
            'new': new
        }
        return render(request, 'contracts.html', context=context)

    def post(self, request, id):
        new = 2
        g_contracts = get_contracts()
        form = ContractsInfoForm(request.POST)
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level in ['m', 'c']:
            new = 1
            g_contracts = g_contracts.filter(Q(client_id=Employee.objects.get(id=request.session["id_user"])) | Q(
                employee_id=Employee.objects.get(id=request.session["id_user"])))
            if Employee.objects.get(
                    id=request.session["id_user"]).access_level == 'c' or ContractOfDevelopment.objects.get(
                    id=id) not in g_contracts.filter(employee_id=Employee.objects.get(id=request.session["id_user"])):
                request.session["message"] = True
                return HttpResponseRedirect('/contracts.html')
            form.fields["employee_id"].required = False
        mod = "редактирование"
        note_id = id
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
            'note_id': note_id,
            'new': new
        }
        if form.is_valid():
            contract = ContractOfDevelopment.objects.get(id=id)
            contract.game_id = form.cleaned_data["game_id"]
            contract.conclusion_date = form.cleaned_data["conclusion_date"]
            contract.contract_end_date = form.cleaned_data["contract_end_date"]
            contract.client_id = form.cleaned_data["client_id"]
            if Employee.objects.get(id=request.session["id_user"]).access_level == 'm':
                contract.employee_id = Employee.objects.get(id=request.session["id_user"])
            else:
                contract.employee_id = form.cleaned_data["employee_id"]
            contract.development_full_price = form.cleaned_data["development_full_price"]
            contract.save()
            return HttpResponseRedirect('/contracts.html')
        else:
            context["error"] = "Неправильное заполнение"
            return render(request, 'contracts.html', context=context)


class ControlPage(View):
    def get(self, request):
        new = False
        if "id_user" not in request.session:
            return HttpResponseRedirect('login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            return HttpResponseRedirect('contracts.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'a':
            new = True
        message = ''
        if "message" in request.session:
            if request.session["message"] == True:
                message = 'Доступ запрещён'
                request.session["message"] = False
            elif request.session["message"] == 2:
                message = 'Нельзя писать сообщения себе'
                request.session["message"] = False
        mod = "добавление"
        g_accounts = get_accounts()
        form = AccountsForm()
        form.fields['access_level'].choices = [('', '---------'), ('m', 'Мастер'), ('c', 'Клиент')]
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
            'new': new,
            'message': message
        }
        return render(request, 'control.html', context=context)

    def post(self, request):
        new = False
        if "id_user" not in request.session:
            return HttpResponseRedirect('login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            return HttpResponseRedirect('contracts.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'a':
            new = True
        message = ''
        if "message" in request.session:
            if request.session["message"] == True:
                message = 'Доступ запрещён'
                request.session["message"] = False
            elif request.session["message"] == 2:
                message = 'Нельзя писать сообщения себе'
                request.session["message"] = False
        mod = "добавление"
        g_accounts = get_accounts()
        form = AccountsForm(request.POST)
        form.fields['access_level'].choices = [('', '---------'), ('m', 'Мастер'), ('c', 'Клиент')]
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
            'new': new,
            'message': message
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
        g_accounts = get_accounts()
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            return HttpResponseRedirect('/contracts.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'm' or g_accounts.get(
                id=id).access_level == 'a':
            request.session["message"] = True
            return HttpResponseRedirect('/control.html')
        mod = "редактирование"
        user_id = id
        avatar = g_accounts.get(id=id).avatar
        form = AccountsForm(initial={'full_name': g_accounts.get(id=id).full_name,
                                     'password': g_accounts.get(id=id).password,
                                     'phone': g_accounts.get(id=id).phone,
                                     'email': g_accounts.get(id=id).email,
                                     'access_level': g_accounts.get(id=id).access_level,
                                     'avatar': g_accounts.get(id=id).avatar})
        form.fields['access_level'].choices = [('', '---------'), ('m', 'Мастер'), ('c', 'Клиент')]
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
        g_accounts = get_accounts()
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            return HttpResponseRedirect('/contracts.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'm' or g_accounts.get(
                id=id).access_level == 'a':
            request.session["message"] = True
            return HttpResponseRedirect('/control.html')
        mod = "редактирование"
        user_id = id
        avatar = g_accounts.get(id=id).avatar
        form = AccountsForm(request.POST, request.FILES)
        form.fields['access_level'].choices = [('', '---------'), ('m', 'Мастер'), ('c', 'Клиент')]
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
        success = ''
        if "id_user" in request.session:
            return HttpResponseRedirect('confirm_exit.html')
        if "success" in request.session:
            if request.session["success"]:
                success = 'Регистрация прошла успешно'
                request.session["success"] = False
        context = {
            'success': success
        }
        return render(request, 'login.html', context=context)

    def post(self, request):
        if "id_user" in request.session:
            return HttpResponseRedirect('confirm_exit.html')
        if "login_user" in request.POST:
            entered_login = request.POST.get("enter_login")
            entered_pass = request.POST.get("enter_pass")
            users = autoriz(entered_login, entered_pass)
            if not users:
                context = {
                    "error": "Введен неверный логин или пароль"
                }
                return render(request, 'login.html', context=context)
            else:
                request.session["id_user"] = users[0].id
                request.session["access"] = users[0].access_level
                return HttpResponseRedirect('account.html')
        if "reg_user" in request.POST:
            form = RegistrateForm(request.POST)
            if form.is_valid():
                entered_confirm = request.POST.get("confirm_pass")
                if form.cleaned_data["password"] == entered_confirm:
                    user = form.save(commit=False)
                    user.access_level = 'c'
                    user.reg_date = datetime.datetime.now()
                    user.save()
                    request.session["success"] = True
                    return HttpResponseRedirect('control.html')
                else:
                    context = {
                        "error": "Повторите пароль"
                    }
                    return render(request, 'login.html', context=context)
            else:
                context = {
                    "error": "Неправильное заполнение"
                }
                return render(request, 'login.html', context=context)


class CreateChat(View):
    def get(self, request, id):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            return HttpResponseRedirect('/contracts.html')
        elif id == request.session["id_user"]:
            request.session["message"] = 2
            return HttpResponseRedirect('/control.html')
        chats = Chat.objects.filter(members__in=[request.session["id_user"], id]).annotate(c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.session["id_user"])
            chat.members.add(id)
        else:
            chat = chats.first()
        return HttpResponseRedirect(reverse('messages', kwargs={'id': chat.id}))


class ChatsPage(View):
    def get(self, request):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        chats = Chat.objects.filter(members__in=[request.session["id_user"]])
        context = {
            'user_profile': Employee.objects.get(id=request.session["id_user"]),
            'chats': chats
        }
        return render(request, 'messages.html', context=context)


class MessagesPage(View):
    def get(self, request, id):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        chats = Chat.objects.filter(members__in=[request.session["id_user"]])
        chat = Chat.objects.get(id=id)
        context = {
            'user_profile': Employee.objects.get(id=request.session["id_user"]),
            'chats': chats,
            'chat': chat,
            'form': MessageForm()
        }
        return render(request, 'messages.html', context=context)

    def post(self, request, id):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = id
            message.sender_id = Employee.objects.get(id=request.session["id_user"])
            message.pub_date = datetime.datetime.now()
            message.save()
        return HttpResponseRedirect(reverse('messages', kwargs={'id': id}))


class ReviewsPage(View):
    def get(self, request):
        if "id_user" in request.session:
            link = "confirm_exit.html"
            log = "Выйти"
        else:
            link = "login.html"
            log = "Войти\Регистрация"
        message = ''
        if "message" in request.session:
            if request.session["message"] == True:
                message = 'Доступ запрещён'
                request.session["message"] = False
        enable = 0
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
            'mod': mod,
            'link': link,
            'log': log,
            'enable': enable,
            'message': message
        }
        return render(request, 'reviews.html', context=context)

    def post(self, request):
        if "id_user" in request.session:
            link = "confirm_exit.html"
            log = "Выйти"
        else:
            link = "login.html"
            log = "Войти\Регистрация"
        message = ''
        if "message" in request.session:
            if request.session["message"] == True:
                message = 'Доступ запрещён'
                request.session["message"] = False
        enable = 0
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
            'mod': mod,
            'link': link,
            'log': log,
            'enable': enable,
            'message': message
        }
        if form.is_valid():
            review = form.save(commit=False)
            review.client_id = Employee.objects.get(id=request.session["id_user"])
            review.public_date = datetime.datetime.now()
            review.save()
            return HttpResponseRedirect('reviews.html')
        else:
            context["error"] = "Неправильное заполнение"
            return render(request, 'reviews.html', context=context)


class ReviewOnePage(View):
    def get(self, request, id):
        link = "confirm_exit.html"
        log = "Выйти"
        enable = 1
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Review.objects.get(id=id).client_id != Employee.objects.get(id=request.session["id_user"]):
            if Employee.objects.get(id=request.session["id_user"]).access_level in ['c', 'm']:
                request.session["message"] = True
                return HttpResponseRedirect('/reviews.html')
            else:
                enable = 2
        mod = "Редактировать"
        review_id = id
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
            'mod': mod,
            'review_id': review_id,
            'link': link,
            'log': log,
            'enable': enable
        }
        return render(request, 'reviews.html', context=context)

    def post(self, request, id):
        link = "confirm_exit.html"
        log = "Выйти"
        enable = 1
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Review.objects.get(id=id).client_id != Employee.objects.get(id=request.session["id_user"]):
            if Employee.objects.get(id=request.session["id_user"]).access_level in ['c', 'm']:
                request.session["message"] = True
                return HttpResponseRedirect('/reviews.html')
            else:
                enable = 2
        mod = "Редактировать"
        review_id = id
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
            'mod': mod,
            'review_id': review_id,
            'link': link,
            'log': log,
            'enable': enable
        }
        if form.is_valid():
            review = Review.objects.get(id=id)
            review.review_text = form.cleaned_data["review_text"]
            review.save()
            return HttpResponseRedirect('/reviews.html')
        else:
            context["error"] = "Неправильное заполнение"
            return render(request, 'reviews.html', context=context)


class StatesPage(View):
    def get(self, request):
        new = False
        g_states = get_states()
        if "id_user" not in request.session:
            return HttpResponseRedirect('login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level in ['a', 'm']:
            new = True
        else:
            g_states = g_states.filter(game_id__in=ContractOfDevelopment.objects.filter(
                client_id=request.session["id_user"]).values_list("game_id", flat=True))
        message = ''
        if "message" in request.session:
            if request.session["message"] == True:
                message = 'Доступ запрещён'
                request.session["message"] = False
        mod = "добавление"
        form = StatesForm()
        filtred = StatesFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_states = g_states.filter(game_id__name__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["ordering"]:
                g_states = g_states.order_by(filtred.cleaned_data["ordering"])

            if filtred.cleaned_data["watching"]:
                if filtred.cleaned_data["watching"] == "a":
                    g_states = g_states.filter(start_date__gt=datetime.datetime.now())
                elif filtred.cleaned_data["watching"] == "b":
                    g_states = g_states.filter(start_date__lt=datetime.datetime.now(),
                                               end_date__gt=datetime.datetime.now())
                elif filtred.cleaned_data["watching"] == "c":
                    g_states = g_states.filter(end_date__lt=datetime.datetime.now())

        context = {
            'g_states': g_states,
            'filtred': filtred,
            'form': form,
            'mod': mod,
            'new': new,
            'message': message
        }
        return render(request, 'game_states.html', context=context)

    def post(self, request):
        new = False
        g_states = get_states()
        if "id_user" not in request.session:
            return HttpResponseRedirect('login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level in ['a', 'm']:
            new = True
        else:
            g_states = g_states.filter(game_id__in=ContractOfDevelopment.objects.filter(
                client_id=request.session["id_user"]).values_list("game_id", flat=True))
        message = ''
        if "message" in request.session:
            if request.session["message"] == True:
                message = 'Доступ запрещён'
                request.session["message"] = False
        mod = "добавление"
        form = StatesForm(request.POST)
        filtred = StatesFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_states = g_states.filter(game_id__name__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["ordering"]:
                g_states = g_states.order_by(filtred.cleaned_data["ordering"])

            if filtred.cleaned_data["watching"]:
                if filtred.cleaned_data["watching"] == "a":
                    g_states = g_states.filter(start_date__gt=datetime.datetime.now())
                elif filtred.cleaned_data["watching"] == "b":
                    g_states = g_states.filter(start_date__lt=datetime.datetime.now(),
                                               end_date__gt=datetime.datetime.now())
                elif filtred.cleaned_data["watching"] == "c":
                    g_states = g_states.filter(end_date__lt=datetime.datetime.now())

        context = {
            'g_states': g_states,
            'filtred': filtred,
            'form': form,
            'mod': mod,
            'new': new,
            'message': message
        }
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('game_states.html')
        else:
            context["error"] = "Неправильное заполнение"
            return render(request, 'game_states.html', context=context)


class StateOnePage(View):
    def get(self, request, id):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            request.session["message"] = True
            return HttpResponseRedirect('/game_states.html')
        mod = "редактирование"
        state_id = id
        g_states = get_states()
        form = StatesForm(initial={'game_id': g_states.get(id=id).game_id,
                                   'start_date': g_states.get(id=id).start_date,
                                   'end_date': g_states.get(id=id).end_date,
                                   'stage_description': g_states.get(id=id).stage_description})
        filtred = StatesFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_states = g_states.filter(game_id__name__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["ordering"]:
                g_states = g_states.order_by(filtred.cleaned_data["ordering"])

            if filtred.cleaned_data["watching"]:
                if filtred.cleaned_data["watching"] == "a":
                    g_states = g_states.filter(start_date__gt=datetime.datetime.now())
                elif filtred.cleaned_data["watching"] == "b":
                    g_states = g_states.filter(start_date__lt=datetime.datetime.now(),
                                               end_date__gt=datetime.datetime.now())
                elif filtred.cleaned_data["watching"] == "c":
                    g_states = g_states.filter(end_date__lt=datetime.datetime.now())

        context = {
            'g_states': g_states,
            'filtred': filtred,
            'form': form,
            'mod': mod,
            'state_id': state_id
        }
        return render(request, 'game_states.html', context=context)

    def post(self, request, id):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            request.session["message"] = True
            return HttpResponseRedirect('/game_states.html')
        mod = "редактирование"
        state_id = id
        g_states = get_states()
        form = StatesForm(request.POST)
        filtred = StatesFilterForm(request.GET)

        if filtred.is_valid():
            if filtred.cleaned_data["search"]:
                g_states = g_states.filter(game_id__name__iregex=filtred.cleaned_data["search"])

            if filtred.cleaned_data["ordering"]:
                g_states = g_states.order_by(filtred.cleaned_data["ordering"])

            if filtred.cleaned_data["watching"]:
                if filtred.cleaned_data["watching"] == "a":
                    g_states = g_states.filter(start_date__gt=datetime.datetime.now())
                elif filtred.cleaned_data["watching"] == "b":
                    g_states = g_states.filter(start_date__lt=datetime.datetime.now(),
                                               end_date__gt=datetime.datetime.now())
                elif filtred.cleaned_data["watching"] == "c":
                    g_states = g_states.filter(end_date__lt=datetime.datetime.now())

        context = {
            'g_states': g_states,
            'filtred': filtred,
            'form': form,
            'mod': mod,
            'state_id': state_id
        }
        if form.is_valid():
            state = GameDevelopmentStage.objects.get(id=id)
            state.game_id = form.cleaned_data["game_id"]
            state.start_date = form.cleaned_data["start_date"]
            state.end_date = form.cleaned_data["end_date"]
            state.stage_description = form.cleaned_data["stage_description"]
            state.save()
            return HttpResponseRedirect('/game_states.html')
        else:
            context["error"] = "Неправильное заполнение"
            return render(request, 'game_states.html', context=context)


class SequrityPage(View):
    def get(self, request):
        if "id_user" not in request.session:
            return HttpResponseRedirect('login.html')
        g_accounts = get_accounts()
        form = SequrityForm(initial={'phone': g_accounts.get(id=request.session["id_user"]).phone,
                                     'email': g_accounts.get(id=request.session["id_user"]).email})
        form.fields["password"].required = False
        conf = PasswordForm()
        context = {
            'form': form,
            'conf': conf
        }
        return render(request, 'sequrity.html', context=context)

    def post(self, request):
        if "id_user" not in request.session:
            return HttpResponseRedirect('login.html')
        g_accounts = get_accounts()
        form = SequrityForm(request.POST)
        form.fields["password"].required = False
        conf = PasswordForm(request.POST)
        context = {
            'form': form,
            'conf': conf
        }
        if form.is_valid() & conf.is_valid():
            user = Employee.objects.get(id=request.session["id_user"])
            user.phone = form.cleaned_data["phone"]
            user.email = form.cleaned_data["email"]
            if form.cleaned_data["password"] != '':
                if conf.cleaned_data["old_pass"] == user.password:
                    if conf.cleaned_data["confirm"] == form.cleaned_data["password"]:
                        user.password = form.cleaned_data["password"]
                    else:
                        context["error"] = "Повторите пароль"
                        return render(request, 'sequrity.html', context=context)
                else:
                    context["error"] = "Текущий пароль введён неверно"
                    return render(request, 'sequrity.html', context=context)
            user.save()
            return HttpResponseRedirect('sequrity.html')
        else:
            context["error"] = "Неправильное заполнение"
            return render(request, 'sequrity.html', context=context)


class ExitPage(View):
    def get(self, request):
        if "id_user" not in request.session:
            return HttpResponseRedirect('login.html')
        context = {}
        return render(request, 'confirm_exit.html', context=context)

    def post(self, request):
        if "id_user" not in request.session:
            return HttpResponseRedirect('login.html')
        request.session.clear()
        context = {}
        return HttpResponseRedirect('/login.html')


class AccountDeletePage(View):
    def get(self, request, id):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            return HttpResponseRedirect('/contracts.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'm' or Employee.objects.get(
                id=id).access_level == 'a':
            return HttpResponseRedirect('/control.html')
        context = {}
        return render(request, 'confirm_delete.html', context=context)

    def post(self, request, id):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            return HttpResponseRedirect('/contracts.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'm' or Employee.objects.get(
                id=id).access_level == 'a':
            return HttpResponseRedirect('/control.html')
        g_del_account = get_del_account(id)
        context = {}
        g_del_account.delete()
        return HttpResponseRedirect('/control.html')


class ContractDeletePage(View):
    def get(self, request, id):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c' or Employee.objects.get(
                id=request.session["id_user"]).access_level == 'm' and ContractOfDevelopment.objects.get(
                id=id).employee_id != Employee.objects.get(id=request.session["id_user"]):
            return HttpResponseRedirect('/contracts.html')
        context = {}
        return render(request, 'confirm_delete.html', context=context)

    def post(self, request, id):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c' or Employee.objects.get(
                id=request.session["id_user"]).access_level == 'm' and ContractOfDevelopment.objects.get(
                id=id).employee_id != Employee.objects.get(id=request.session["id_user"]):
            return HttpResponseRedirect('/contracts.html')
        g_del_contract = get_del_contract(id)
        context = {}
        g_del_contract.delete()
        return HttpResponseRedirect('/contracts.html')


class GameDeletePage(View):
    def get(self, request, id):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            return HttpResponseRedirect('/contracts.html')
        context = {}
        return render(request, 'confirm_delete.html', context=context)

    def post(self, request, id):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            return HttpResponseRedirect('/contracts.html')
        g_del_game = get_del_game(id)
        context = {}
        g_del_game.delete()
        return HttpResponseRedirect('/allgames.html')


class TaskDeletePage(View):
    def get(self, request, id):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            return HttpResponseRedirect('/contracts.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'm':
            return HttpResponseRedirect('/alltasks.html')
        context = {}
        return render(request, 'confirm_delete.html', context=context)

    def post(self, request, id):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            return HttpResponseRedirect('/contracts.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'm':
            return HttpResponseRedirect('/alltaks.html')
        g_del_task = get_del_task(id)
        context = {}
        g_del_task.delete()
        return HttpResponseRedirect('/alltasks.html')


class StateDeletePage(View):
    def get(self, request, id):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            return HttpResponseRedirect('/game_states.html')
        context = {}
        return render(request, 'confirm_delete.html', context=context)

    def post(self, request, id):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Employee.objects.get(id=request.session["id_user"]).access_level == 'c':
            return HttpResponseRedirect('/game_states.html')
        g_del_state = get_del_state(id)
        context = {}
        g_del_state.delete()
        return HttpResponseRedirect('/game_states.html')


class ReviewDeletePage(View):
    def get(self, request, id):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Review.objects.get(id=id).client_id != Employee.objects.get(id=request.session["id_user"]) and Employee.objects.get(id=request.session["id_user"]).access_level in ['c', 'm']:
            return HttpResponseRedirect('/reviews.html')
        context = {}
        return render(request, 'confirm_delete.html', context=context)

    def post(self, request, id):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Review.objects.get(id=id).client_id != Employee.objects.get(id=request.session["id_user"]) and Employee.objects.get(id=request.session["id_user"]).access_level in ['c', 'm']:
            return HttpResponseRedirect('/reviews.html')
        g_del_review = get_del_review(id)
        context = {}
        g_del_review.delete()
        return HttpResponseRedirect('/reviews.html')


class MessageDeletePage(View):
    def get(self, request, id):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Message.objects.get(id=id).sender_id != Employee.objects.get(id=request.session["id_user"]):
            return HttpResponseRedirect('/messages.html')
        context = {}
        return render(request, 'confirm_delete.html', context=context)

    def post(self, request, id):
        if "id_user" not in request.session:
            return HttpResponseRedirect('/login.html')
        elif Message.objects.get(id=id).sender_id != Employee.objects.get(id=request.session["id_user"]):
            return HttpResponseRedirect('/messages.html')
        g_del_message = get_del_message(id)
        context = {}
        g_del_message.delete()
        return HttpResponseRedirect('/messages.html')
