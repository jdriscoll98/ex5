from django.urls import path
from . import views

app_name = "app"
urlpatterns = [
    path("", views.home, name="home"),
    path("us_cases/", views.us_cases, name="us_cases"),
    path(
        "avg_cases_and_deaths/",
        views.avg_cases_and_deaths,
        name="avg_cases_and_deaths",
    ),
]
