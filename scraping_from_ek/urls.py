from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('list', views.home_list, name='home_list'),
    path('list-filter', views.home_list_filter, name='home_list_filter'),

]