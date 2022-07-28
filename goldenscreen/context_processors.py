from repertoire.models import Cinema
from django.core.serializers import serialize
def cinema_list(request):
    cinemas = Cinema.objects.all()
    return {
        'cinemas': cinemas
    }
def cinemas_geolocation(request):
    cinemas = Cinema.objects.all()
    cinemas = serialize('json', cinemas, fields=['id', 'name', 'geolocation'])
    return {
        'cinemasLocations': cinemas
    }