from django.urls import path
from . import views

urlpatterns = [    
    path("login", views.login, name="login"),
    path("questionaire", views.questionaire, name="questionaire"),
    path("dashboard", views.dashboard, name="signup"),
    path("report/<str:report_code>", views.report, name="report"),
    path("join_report/<str:user_code>/<str:inviter_code>/<str:report_code>/", views.join_report, name="jreport"),

    path("logout", views.logout, name="signup"),
    path("", views.dashboard, name="dashboard"),

]