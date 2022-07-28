import datetime
from datetime import timedelta, date
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from library.models import Movie
from django.utils.text import slugify
from django_google_maps.fields import AddressField, GeoLocationField

DEFAULT_CINEMA_ID = 1

class Cinema(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = AddressField(max_length=200)
    geolocation = GeoLocationField(max_length=100, unique=True)
    def __str__(self):
        return self.name

def default_seats_dict():
    return {'str': 'Automaticly filled'}

class Hall(models.Model):
    name = models.CharField(max_length=200, default="")
    cinema = models.ForeignKey(Cinema, default=DEFAULT_CINEMA_ID, on_delete=models.CASCADE)
    seats = models.JSONField()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name','cinema'], name='same_name_cinema')
        ]
    def __str__(self):
        return self.cinema.name + " - Sala " + self.name
		
class Time(models.Model):
    time = models.TimeField(unique=True)
    def __str__(self):
        return self.time.strftime("%H:%M:%S")
        
class Seans(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, help_text='Wybierz film, który będzie seansem',on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, help_text='Wybierz salę w której odbędzie się seans',on_delete=models.CASCADE)
    seats = models.JSONField(default=default_seats_dict)
    slug = models.SlugField(default="automaticly-filled", blank=True)
    showingDate = models.DateField(validators=[MinValueValidator(datetime.date.today)])
    showingHour = models.ForeignKey(Time, help_text='Wybierz godzinę projekcji filmu',on_delete=models.CASCADE)
    futureDays = models.IntegerField(validators=[MinValueValidator(0)], blank=True, default=0)
    class Meta:
        verbose_name = 'Showing'
        verbose_name_plural = 'Showings'
        constraints = [
            models.UniqueConstraint(fields=['movie','hall','showingDate', 'showingHour'], name='showing_contraints'),
            models.UniqueConstraint(fields=['hall','showingDate', 'showingHour'], name='same_hall_date_showing')
        ]
    def __str__(self):
        return self.movie.title + " - " + str(self.hall) + "  " + str(self.showingDate) + "  " + str(self.showingHour)
		
    def save(self, *args, **kwargs):
        self.slug = slugify(self)
        self.seats = self.hall.seats
        fd = self.futureDays
        self.futureDays = 0
        super(Seans, self).save(*args, **kwargs)
        if fd > 0:
            i = 0
            while i < fd:
                newShowing = Seans(movie=self.movie,hall=self.hall,seats=self.seats,slug=self.slug,showingDate=self.showingDate + timedelta(days=i+1)
                ,showingHour=self.showingHour, futureDays=0)
                newShowing.save()
                i = i + 1
		
    def saveSeats(self, *args, **kwargs):
	    super(Seans, self).save(*args, **kwargs)
        
