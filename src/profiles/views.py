from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


User = get_user_model()


@login_required
def profile_list_view(request, *args, **kwargs):
    context = {
        "object_list": User.objects.filter(is_active=True)
    }
    return render(request, 'profiles/list.html', context)

# Create your views here.
@login_required
def profile_detail_view(request, *args, **kwargs):
    # # To see the permissions.
    # print("auth.view_user", request.user.has_perm("auth.view_user"))
    # print("visits.view_pagevisit", request.user.has_perm("visits.view_pagevisit"))

    # Other options are.
    # refer : https://docs.djangoproject.com/en/5.1/topics/auth/default/#default-permissions
    # <app_label>.view_<model_name>
    # <app_label>.add_<model_name>
    # <app_label>.delete_<model_name>
    # <app_label>.change_<model_name>

    user_object = get_object_or_404(User, username=kwargs['username'])
    # return HttpResponse(f"Hello there {kwargs['username']} - {user_object.id}")
    owner = user_object == request.user
    context = {
        "instance" : user_object,
        "owner": owner

    }
    return render(request, 'profiles/details.html', context)