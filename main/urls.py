from django.urls import path
from . import views

urlpatterns = [    
    path("login", views.login, name="login"),
    
    path("dashboard", views.dashboard, name="signup"),
    path("logout", views.logout, name="signup"),
    path("", views.dashboard, name="dashboard"),

]