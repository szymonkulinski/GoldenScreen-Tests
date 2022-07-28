import datetime
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

def get_img_upload_path(instance, filename):
    return f'media/{instance.title}/{filename}'

def get_imgs_path(instance, filename):
    return f'media/{instance.path}/{filename}'


	
class MovieImage(models.Model):
    path = models.CharField(max_length=100, help_text='Wpisz nazwę filmu (dla organizacji obrazków)')
    image = models.ImageField(upload_to=get_imgs_path)
    def __str__(self):
        img = self.image.name.split("/",1)[1]
        return img.split("/",2)[1]

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Wpisz nazwę kategorii', unique=True)
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200, help_text='Wpisz nazwę filmu')
    description = models.TextField(max_length=300, help_text='Wpisz opis filmu')

    productionCountry = models.CharField(max_length=100, help_text='Podaj kraj produkcji', default='')
    director = models.CharField(max_length=300, help_text='Podaj reżysera filmu', default='')
    screenwriter = models.CharField(max_length=300, help_text='Podaj scenarzystę filmu', default='')
    cast = models.TextField(max_length=300, help_text='Podaj główną obsadę filmu', default='')
    trailer = models.CharField(max_length=150, help_text='Podaj embedded (do umiejscowienia na stronie) URL zwiastunu', default='/')
    
    images = models.ManyToManyField(MovieImage, help_text='Wybierz obrazki filmu')
    genre = models.ManyToManyField(Genre, help_text='Wybierz kategorię filmu')

    slug = models.SlugField(default="")
    releaseDate = models.DateField(auto_now=False, auto_now_add=False, blank=False, default=datetime.date.today)
    length = models.IntegerField(validators=[MinValueValidator(5)], blank=True, default=5)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title','releaseDate'], name='title_releaseDate')
        ]
    def __str__(self):
        return self.title
    
    def poster(self):
        for image in self.images.all():
            if str(image).find("poster") != -1 or str(image).find("Poster") != -1:
                return image
        return self.images.first



class UserOpinion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], blank=False, default=0)
    review = models.TextField(max_length=500, default='', blank=True)
    createdDate = models.DateField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'movie'], name='userMovieConstraint')
        ]
    def __str__(self):
         return self.user.username + " " + self.movie.title + " - " + str(self.rating)
