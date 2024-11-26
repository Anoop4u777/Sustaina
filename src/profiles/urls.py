from django.urls import path

from .views import (profile_detail_view, profile_list_view)

urlpatterns = [
    path('', profile_list_view),
    path('<username>/details/', profile_detail_view),
]
