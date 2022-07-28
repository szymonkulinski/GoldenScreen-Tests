from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render
from datetime import datetime
from .models import Hall, Seans, Cinema
from library.models import Genre, Movie, UserOpinion
from .forms import UserFinalizationForm

def mainPage(request):
    request.session['movieReservation'] = False
    if 'cinemaName' not in request.session:
        request.session['cinemaName'] = "Mapa kin"
    if request.method == 'POST':
        if 'cinemaName' in request.POST:
            request.session['cinemaName'] = request.POST['cinemaName']
            if request.POST['cinemaName'] == "Mapa kin":
                return render(request,
                 'repertoire/cinemaMap.html')
    else:
        if request.session['cinemaName'] == 'Mapa kin':
            return render(request,
                 'repertoire/cinemaMap.html')
    current_date = datetime.now()
    _movies = Seans.objects.all().values('movie__title', 'movie__images__image', 'movie__slug', 'movie__genre__name' , 'movie__description', 'movie__length', 'movie__releaseDate').filter(hall__cinema__name=request.session['cinemaName'], showingDate__gte=current_date.date()).distinct()
    movies = []
    movie_name = ""
    for movie in _movies:
        if movie_name != movie['movie__title']:
            _movie = Movie.objects.get(title=movie['movie__title'])
            query = Seans.objects.filter(movie=_movie, hall__cinema__name=request.session['cinemaName'], showingDate__gte=current_date.date())
            if query:
                days = query.values('showingDate__day', 'showingDate__month').order_by('showingDate__year', 'showingDate__month', 'showingDate__day').filter(showingDate__gte=current_date.date()).distinct()
                if days.count() > 0:
                    movie_name = movie['movie__title']
                    movies.append(movie)
    if movies:
        newestShowing = movies[0]
        return render(request,
                 'repertoire/mainPage.html',
                  {'movies': movies, 'newestShowing': newestShowing})
    else:
        #no showings screen
        return render(request,
                 'repertoire/mainPage404.html')
				    
def movie_detail(request, slug):
    request.session['movieReservation'] = False
    if 'cinemaName' not in request.session:
        request.session['cinemaName'] = "Mapa kin"
    if request.method == 'POST':
        if 'cinemaName' in request.POST:
            request.session['cinemaName'] = request.POST['cinemaName']
            if request.POST['cinemaName'] == "Mapa kin":
                return render(request,
                 'repertoire/cinemaMap.html')
    else:
        if request.session['cinemaName'] == 'Mapa kin':
            return render(request,
                 'repertoire/cinemaMap.html')
    movie = Movie.objects.get(slug=slug)
    query = Seans.objects.filter(movie=movie, hall__cinema__name=request.session['cinemaName'])
    avrRating = 0.0
    message = ''
    if request.method == 'POST' and request.user.is_authenticated:
        if 'selectRating' in request.POST:
            rating = request.POST['selectRating']
            review = request.POST['textRating']
            if int(rating) > 0 and int(rating) < 6 and len(review) <= 500:
                try:
                    obj, created = UserOpinion.objects.get_or_create(user=request.user,movie=movie,rating=int(rating), review=review)
                    message = "Dodano nową opinię!"
                except IntegrityError as e:
                    message = "Nie można dodać dwóch opinii do jednego filmu!"
            else:
                if len(review) > 500:
                    message = "Zbyt długa recenzja! Spróbuj ją skrócić."
                else:
                    message = "Nie poprawna wartość!"
        elif 'selectRatingEdit' in request.POST:
            op = UserOpinion.objects.get(user=request.user, movie=movie)
            oldRating = op.rating
            oldReview = op.review
            rating = request.POST['selectRatingEdit']
            review = request.POST['textRatingEdit']
            if oldRating == int(rating) and oldReview == review:
                message = "Nie zmieniono opinii!"
            else:
                if int(rating) > 0 and int(rating) < 6 and len(review) <= 500:
                    op.rating = rating
                    op.review = review
                    op.save()
                    message = "Zaktualizowano opinię!"
                else:
                    if len(review) > 500:
                        message = "Zbyt długa recenzja! Spróbuj ją skrócić."
                    else:
                        message = "Nie poprawna wartość!"
        
    opinions = UserOpinion.objects.filter(movie=movie).order_by("-id")
    
    if request.user.is_authenticated:
        opinion = UserOpinion.objects.filter(user=request.user, movie=movie)
    else:
        opinion = None

    if opinions.count() > 0:
        for _opinion in opinions:
            avrRating = avrRating + _opinion.rating
        avrRating = avrRating / opinions.count()
        avrRating = round(avrRating, 1)
    else:
        avrRating = "Brak"

    if query:
        current_date = datetime.now()
        days_list = query.values('showingDate__day', 'showingDate__month').order_by('showingDate__year', 'showingDate__month', 'showingDate__day').filter(showingDate__gte=current_date.date()).distinct()
        
        page = request.GET.get('page', 1)
        paginator = Paginator(days_list, 6)
        try:
            days = paginator.page(page)
        except PageNotAnInteger:
            days = paginator.page(1)
        except EmptyPage:
            days = paginator.page(paginator.num_pages)
        if opinion != None:
            return render(request,
                        'repertoire/movie_detail.html', 
                        {'opinion': opinion, 'current_date': current_date,'movie': movie, 'query': query, 'days': days, 'opinions': opinions, 'avrRating': avrRating, 'message': message})
        else:
            return render(request,
                        'repertoire/movie_detail.html', 
                        {'current_date': current_date,'movie': movie, 'query': query, 'days': days, 'opinions': opinions, 'avrRating': avrRating, 'message': message})
    else:
        if opinion != None:
            return render(request,
                      'repertoire/movie_detail.html', 
                      {'opinion':opinion, 'movie': movie, 'opinions': opinions, 'avrRating': avrRating, 'message': message})
        else:        
            return render(request,
                        'repertoire/movie_detail.html', 
                        {'movie': movie, 'opinions': opinions, 'avrRating': avrRating, 'message': message})
					  
					
def movie_reservation(request, slug):
    request.session['movieReservation'] = True
    showing = Seans.objects.get(slug=slug)
    if request.method == 'POST':
        if 'finalize' in request.POST:
            seats = request.POST.getlist("seats")
            form = UserFinalizationForm(request.POST)
            if form.is_valid():
                for seat in seats:
                    seat = seat.split(".")
                    row = int(seat[0])
                    column = int(seat[1])
                    if showing.seats[row]['seats'][column]['isTaken'] == False:
                        showing.seats[row]['seats'][column]['isTaken'] = True
                        showing.saveSeats()
                    else:
                        message = "Twoje miejsca zostały już zarezerwowane. Wybierz jeszcze raz inne miejsca!"
                        return render(request,
                        'repertoire/movie_reservation.html',
                      {'showing': showing, 'message': message})
                return render(request,
                     'repertoire/movie_reservation.html',
                      {'showing': showing})
            else:
                if request.POST.get('logged'):
                    for seat in seats:
                        seat = seat.split(".")
                        row = int(seat[0])
                        column = int(seat[1])
                        if showing.seats[row]['seats'][column]['isTaken'] == False:
                            showing.seats[row]['seats'][column]['isTaken'] = True
                            showing.saveSeats()
                    return render(request,
                        'repertoire/movie_reservation.html',
                        {'showing': showing})
                else:
                    chosenSeats = []
                    for seat in seats:
                        seat = seat.split(".")
                        row = int(seat[0])
                        column = int(seat[1])
                        chosenSeat = str("Rząd: " + str(row+1) + " " + "Siedzenie: " + str(column+1))
                        chosenSeats.append(chosenSeat)
                    return render(request,
                        'repertoire/movie_finalization.html',
                        {'showing': showing, 'chosenSeats': chosenSeats, 'seats': seats, 'form': form})
            

        elif 'confirmSeats' in request.POST: 
            seats = request.POST.getlist("seats")
            form = UserFinalizationForm()
            chosenSeats = []
            for seat in seats:
                seat = seat.split(".")
                row = int(seat[0])
                column = int(seat[1])
                chosenSeat = str("Rząd: " + str(row+1) + " " + "Siedzenie: " + str(column+1))
                chosenSeats.append(chosenSeat)
            return render(request,
                     'repertoire/movie_finalization.html',
                      {'showing': showing, 'chosenSeats': chosenSeats, 'seats': seats, 'form': form})
        
    else:
        return render(request,
                     'repertoire/movie_reservation.html',
                      {'showing': showing})

