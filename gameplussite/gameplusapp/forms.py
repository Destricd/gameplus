from django import forms


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
