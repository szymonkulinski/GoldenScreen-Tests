from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.mainPage, name='mainPage'),
	path('admin/', admin.site.urls),
	path('repertoire/', include('repertoire.urls'), name='repertoire'),
	path('account/', include('account.urls'), name='account'),
	path('library/', include('library.urls'), name='library'),
	path('social-auth/', include('social_django.urls', namespace='social')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)