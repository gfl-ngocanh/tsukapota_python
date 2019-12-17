from django.urls import path

from . import views

app_name = 'tsukapota'

urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
]