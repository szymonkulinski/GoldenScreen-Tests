from django.urls import path, include
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
app_name = 'account'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
	path('', include('django.contrib.auth.urls')),
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('account:password_change_done')), name='password_change'),
    path('email-change/', views.email_change, name='email_change'),
    path('deactivate/', views.deactivate_account, name='deactivate_account'),
    path('register/', views.register, name='register'),
]

