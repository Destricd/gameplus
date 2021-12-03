"""gameplussite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from gameplusapp.views import *
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPage.as_view()),
    path('games.html', GamesPage.as_view()),
    path('games.html/<int:id>', GameOnePage.as_view()),
    path('games.html/<int:id>/contract', CreateContract.as_view()),
    path('account.html', AccountPage.as_view()),
    path('allgames.html', AllGamesPage.as_view()),
    path('allgames.html/<int:id>', GameListOnePage.as_view()),
    path('allgames.html/<int:id>/delete', GameDeletePage.as_view()),
    path('alltasks.html', AllTasksPage.as_view()),
    path('alltasks.html/<int:id>', TaskOnePage.as_view()),
    path('alltasks.html/<int:id>/delete', TaskDeletePage.as_view()),
    path('contracts.html', ContractsPage.as_view()),
    path('contracts.html/<int:id>', ContractOnePage.as_view()),
    path('contracts.html/<int:id>/delete', ContractDeletePage.as_view()),
    path('control.html', ControlPage.as_view()),
    path('control.html/<int:id>', ControlOnePage.as_view()),
    path('control.html/<int:id>/delete', AccountDeletePage.as_view()),
    path('game_states.html', StatesPage.as_view()),
    path('game_states.html/<int:id>', StateOnePage.as_view()),
    path('game_states.html/<int:id>/delete', StateDeletePage.as_view()),
    path('login.html', LoginPage.as_view()),
    path('confirm_exit.html', ExitPage.as_view()),
    path('messages.html', ChatsPage.as_view()),
    path('messages.html/<int:id>', MessagesPage.as_view(), name='messages'),
    path('messages.html/create/<int:id>', CreateChat.as_view()),
    path('messages.html/<int:id>/delete', MessageDeletePage.as_view()),
    path('reviews.html', ReviewsPage.as_view()),
    path('reviews.html/<int:id>', ReviewOnePage.as_view()),
    path('reviews.html/<int:id>/delete', ReviewDeletePage.as_view()),
    path('sequrity.html', SequrityPage.as_view())
]
