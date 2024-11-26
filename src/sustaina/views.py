import pathlib
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

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
    return render(request, "base.html", context=my_context)

VALID_CODE="abc123"

def pw_protected_view(request, *args, **kwargs):
    is_allowed = request.session.get('protected_page_allowed', 0)
    if request.method == "POST":
        user_pw_code = request.POST.get("code") or None
        if user_pw_code == VALID_CODE:
            is_allowed = 1
            request.session['protected_page_allowed'] = is_allowed
    if is_allowed:
        return render(request, 'protected/view.html', {})
    return render(request, 'protected/entry.html', {})

@login_required
def user_only_view(request, *args, **kwargs):
    return render(request, 'protected/user-only.html', {})

@staff_member_required()
def staff_only_view(request, *args, **kwargs):
    return render(request, 'protected/user-only.html', {})
