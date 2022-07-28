from django.urls import path, include
from . import views
app_name = 'library'
urlpatterns = [
    path('', views.movieLibrary, name='movieLibrary'),
    path('ranking/', views.movieRanking, name='movieRanking'),
]
