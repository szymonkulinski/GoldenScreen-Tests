import json 
from django.contrib import admin
from django.forms.widgets import TextInput
from .models import Hall, Seans, Time, Cinema
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

class CinemaAdmin(admin.ModelAdmin): formfield_overrides = {
    map_fields.AddressField: { 'widget':
    map_widgets.GoogleMapsAddressWidget(attrs={
      'data-autocomplete-options': json.dumps({ 'types': ['geocode',
      'establishment'], 'componentRestrictions': {
                  'country': 'pl'
              }
          })
      })
    },
    map_fields.GeoLocationField: { 
        'widget': TextInput(attrs={
            'readonly': 'readonly'
        })
    },
}
def reset_seats(modeladmin, request, queryset):
    for hall in queryset.all():
        for x in hall.seats:
            for seat in x['seats']:
                seat['isTaken'] = False
                seat['selected'] = False
        hall.save()
reset_seats.short_description = "Mark selected halls to clear seats"

def reset_seats_showing(modeladmin, request, queryset):
    for showing in queryset.all():
        for x in showing.seats:
            for seat in x['seats']:
                seat['isTaken'] = False
                seat['selected'] = False
        showing.save()
reset_seats_showing.short_description = "Mark showings to clear seats"

class HallAdmin(admin.ModelAdmin):
    actions = [reset_seats]

class SeansAdmin(admin.ModelAdmin):
    actions = [reset_seats_showing]

# Register your models here.
admin.site.register(Seans, SeansAdmin)
admin.site.register(Hall, HallAdmin)
admin.site.register(Cinema, CinemaAdmin)
admin.site.register(Time)


