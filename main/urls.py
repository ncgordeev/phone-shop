from django.urls import path

from main.apps import MainConfig
from main.views import BaseView, UserCreateView

app_name = MainConfig.name

urlpatterns = [
    # path('', BaseView.as_view(), name='base'),
    path('', UserCreateView.as_view(), name='create_user'),
]
