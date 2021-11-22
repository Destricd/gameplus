from django

class GamesFilterForm(forms.Form):
    gamesort = forms.ChoiceField(label="сортировка", required=False, choices=[
        ["name", "по алфавиту"],
        ["date", "по дате"],
        ["price", "по цене с дешёвой"],
        ["-price", "по цене с дорогой"]
    ])