from django.urls import path, include
from . import views
app_name = 'repertoire'
urlpatterns = [
    path('', views.mainPage, name='mainPage'),
	path('<slug:slug>/', views.movie_detail, name='movie_detail'),
	path('reservation/<slug:slug>/', views.movie_reservation, name='movie_reservation'),
]
