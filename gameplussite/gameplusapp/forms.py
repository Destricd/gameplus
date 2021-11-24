from django import forms
from .models import ContractOfDevelopment
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
