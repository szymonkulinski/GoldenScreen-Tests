from django.shortcuts import render
from .models import Genre, Movie, UserOpinion

def movieRanking(request):
    data = Movie.objects.all()
    return render(request,
                  'library/movieRanking.html',
                  {'data': data})

def movieLibrary(request):
    request.session['movieReservation'] = True
    data = Movie.objects.all()
    moviesRatings = []
    for movie in data:
        avrRating = 0.0
        opinions = UserOpinion.objects.filter(movie=movie)
        if opinions.count() > 0:
            for opinion in opinions:
                avrRating = avrRating + opinion.rating
            avrRating = avrRating / opinions.count()
            avrRating = round(avrRating, 1)
        if avrRating < 1:
            moviesRatings.append("Brak")
        else:
            moviesRatings.append(avrRating)
    return render(request,
                  'library/movieLibrary.html',
                  {'data': data, 'moviesRatings': moviesRatings})