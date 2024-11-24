import pathlib
from django.shortcuts import render
from django.http import HttpResponse

from visits.models import PageVisit

this_dir = pathlib.Path(__file__).resolve().parent

def home_page(request, *args, **kwargs):
    queryset = PageVisit.objects.all().count()
    PageVisit.objects.create(path=request.path)
    return render(request, "home.html", {"page_title":"Hai test title", "queryset": queryset})