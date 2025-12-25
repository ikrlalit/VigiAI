from django.urls import path
from apis import views


urlpatterns = [
    path('AddEvent', views.AddEvent_f, name='AddEvent'),
    path('AlertsList', views.AlertsList_f, name='AlertsList'),
    path('AlertStatusUpdate', views.AlertStatusUpdate_f, name='AlertStatusUpdate'),
    path('UserLogin', views.UserLogin_f, name='UserLogin'),
    path('AddNewUser', views.AddNewUser_f, name='AddNewUser'),
    ]