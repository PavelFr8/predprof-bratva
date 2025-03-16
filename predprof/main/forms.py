import django.forms


class UrlForm(django.forms.Form):
    url = django.forms.CharField(
        label="Адрес получения данных",
        help_text="Введите адрес получения данных",
        required=True,
        widget=django.forms.TextInput(attrs={"class": "form-control"}),
    )
