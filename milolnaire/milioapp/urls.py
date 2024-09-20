from django.urls import path
from milioapp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("game/", views.game, name="game"),
    path("start_game/", views.start_game, name="start_game"),
    path("congratulations/", views.congratulations, name="congratulations"),
]