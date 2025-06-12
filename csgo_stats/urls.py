from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_player, name='search_player'),
    path('player/<str:player_id>/', views.player_detail, name='player_detail'),
    path('match/<str:match_id>/', views.match_detail, name='match_detail'),
]
