from django.shortcuts import render
from django.conf import settings
from django.contrib import messages

from main.forms import UrlForm
from main.utils import create_plot


def main(request):
    url_form = UrlForm(request.POST or None)
    context = {
        "url_form": url_form,
        "img": ""
    }
    if request.method == "POST":
        if url_form.is_valid():
            settings.API_URL = url_form.cleaned_data.get("url")
            print(settings.API_URL)
            if create_plot():
                messages.success(
                    request,
                    "Форма успешно отправлена!",
                )
            else:
                messages.success(
                    request,
                    "Неверный адрес!",
                )
    return render(request, "index.html", context)
