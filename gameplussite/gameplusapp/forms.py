from django import forms
from .models import Game
from .models import ContractOfDevelopment
from .models import Employee
from .models import Review


class GamesFilterForm(forms.Form):
    ordering = forms.ChoiceField(required=False, widget=forms.Select(attrs={
        'class': 'sortsel'
    }), choices=[
        ["name", "Алфавиту"],
        ["release_date", "Дате выхода"],
        ["price", "Цене с дешёвой"],
        ["-price", "Цене с дорогой"]
    ])
    search = forms.CharField(label="Найти:", required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Искать здесь...'
    }))


class GamesForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'type', 'rate', 'rules', 'release_date', 'site', 'number_of_rules', 'price', 'development_budget', 'picture']

        widgets = {
            "name": forms.TextInput(attrs={
                'placeholder': 'Название'
            }),
            "type": forms.TextInput(attrs={
                'placeholder': 'Жанр'
            }),
            "rate": forms.TextInput(attrs={
                'placeholder': 'Рекомендуемый возраст'
            }),
            "rules": forms.Textarea(attrs={
                'placeholder': 'Полное описание'
            }),
            "site": forms.TextInput(attrs={
                'placeholder': 'Сайт игры'
            }),
            "price": forms.NumberInput(attrs={
                'placeholder': 'Цена, руб.'
            }),
            "development_budget": forms.NumberInput(attrs={
                'placeholder': 'Бюджет, руб.'
            })
        }


class ContractsForm(forms.ModelForm):
    class Meta:
        model = ContractOfDevelopment
        fields = ['conclusion_date', 'contract_end_date', 'employee_id', 'client_id', 'development_full_price']

        widgets = {
            "development_full_price": forms.NumberInput(attrs={
                'placeholder': 'Дополнительные расходы, руб.'
            })
        }


class ReviewsFilterForm(forms.Form):
    ordering = forms.ChoiceField(required=False, widget=forms.Select(attrs={
        'class': 'sortsel'
    }), choices=[
        ["-public_date", "Дате последней публикации"],
        ["public_date", "Дате первой публикации"]
    ])
    search = forms.CharField(label="Найти:", required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Искать здесь...'
    }))


class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['client_id', 'review_text']

        widgets = {
            "review_text": forms.Textarea(attrs={
                'placeholder': 'Пишите свои пожелания и замечания для улучшения нашего сервиса, делитесь впечатлениями'
            })
        }


class AccountsFilterForm(forms.Form):
    watching = forms.ChoiceField(required=False, widget=forms.Select(attrs={
        'class': 'sortsel'
    }), choices=[
        ["", "Всех"],
        ["a", "Админов"],
        ["m", "Сотрудников"],
        ["c", "Клиентов"]
    ])
    ordering = forms.ChoiceField(required=False, widget=forms.Select(attrs={
        'class': 'sortsel'
    }), choices=[
        ["-reg_date", "Дате последней регистрации"],
        ["reg_date", "Дате первой регистрации"],
        ["full_name", "ФИО"],
        ["login", "Логинам"]
    ])
    search = forms.CharField(label="Найти:", required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Искать здесь...'
    }))


class AccountsForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'phone', 'access_level', 'email', 'login', 'password', 'avatar']

        widgets = {
            "full_name": forms.TextInput(attrs={
                'placeholder': 'Фамилия Имя Отчество'
            }),
            "phone": forms.NumberInput(attrs={
                'placeholder': '***********'
            }),
            "email": forms.EmailInput(attrs={
                'placeholder': 'box@example.com'
            }),
            "login": forms.TextInput(attrs={
                'placeholder': 'Логин'
            }),
            "password": forms.PasswordInput(attrs={
                'placeholder': 'Пароль'
            }, render_value=True)

        }


class ContractsFilterForm(forms.Form):
    watching = forms.ChoiceField(required=False, widget=forms.Select(attrs={
        'class': 'sortsel'
    }), choices=[
        ["", "Все"],
        ["a", "Неподписанные"],
        ["b", "Действующие"],
        ["c", "Расторгнутые"]
    ])
    ordering = forms.ChoiceField(required=False, widget=forms.Select(attrs={
        'class': 'sortsel'
    }), choices=[
        ["game_id", "Играм"],
        ["conclusion_date", "Дате подписания"],
        ["contract_end_date", "Дате окончания срока действия"],
        ["employee_id", "Оформителям"]
    ])
    search = forms.CharField(label="Найти:", required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Искать здесь...'
    }))


class ContractsInfoForm(forms.ModelForm):
    class Meta:
        model = ContractOfDevelopment
        fields = ['game_id', 'conclusion_date', 'contract_end_date', 'client_id', 'employee_id', 'development_full_price']

        widgets = {
            "development_full_price": forms.NumberInput(attrs={
                'placeholder': 'Дополнительные расходы, руб.'
            })

        }
