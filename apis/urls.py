from django.urls import path
from apis import views


urlpatterns = [
    path('AddEvent', views.AddEvent_f, name='AddEvent'),
    path('AlertsList', views.AlertsList_f, name='AlertsList'),
    ]