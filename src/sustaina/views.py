import pathlib
from django.shortcuts import render
from django.http import HttpResponse

from visits.models import PageVisit

this_dir = pathlib.Path(__file__).resolve().parent

def home_view(request, *args, **kwargs):
    return about_view(request, *args, **kwargs)

def about_view(request, *args, **kwargs):
    queryset = PageVisit.objects.all()
    page_queryset = PageVisit.objects.filter(path=request.path)
    try:
        percent = (page_queryset.count() * 100.0 / queryset.count())
    except:
        percent = 0

    PageVisit.objects.create(path=request.path)

    my_context = {
        "page_title":"Hai test title",
        "page_visit_count": page_queryset.count(),
        "percent" : percent,
        "total_visit": queryset.count()
        }
    return render(request, "about.html", context=my_context)