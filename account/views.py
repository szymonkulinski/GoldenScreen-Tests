from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import LoginForm, UserRegistrationForm, ChangeEmailForm, DeactivateForm
from django.contrib import messages

@login_required
def dashboard(request):
    request.session['movieReservation'] = True
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})

@login_required
def email_change(request):
    request.session['movieReservation'] = True
    if request.method == 'POST':
        user = request.user
        form = ChangeEmailForm(user, request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=user.username,
                                password=cd['password'])
            if user is not None:
                form.save()
                return render(request,
                    'account/dashboard.html',
                    {'section': 'dashboard'})
            else:
                message = 'Błędne hasło.'
                return render(request,
                    'account/email_change_form.html',
                    {'form': form, 'message': message})
    else:
        form = ChangeEmailForm(user=request.user)
    return render(request,
                    'account/email_change_form.html',
                    {'form': form})

@login_required
def deactivate_account(request):
    request.session['movieReservation'] = True
    if request.method == 'POST':
        form = DeactivateForm(request.POST)
        if form.is_valid():
            user = request.user
            cd = form.cleaned_data
            user = authenticate(request,
                                username=user.username,
                                password=cd['password'])
            if user is not None:
                user.is_active = False
                user.save()
                logout(request)
                messages.info(request, 'Poprawnie deaktywowano konto.')
                return redirect('repertoire:mainPage')
            else:
                message = 'Błędne hasło.'
                return render(request,
                    'account/deactivate_account.html',
                    {'form': form, 'message': message})
    else:
        form = DeactivateForm()
    return render(request,
                    'account/deactivate_account.html',
                    {'form': form})
    
    

def register(request):
    request.session['movieReservation'] = True
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            
            new_user.set_password(
                user_form.cleaned_data['password'])
            
            new_user.save()
            
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})

#not used - need to change urls
def user_login(request):
    request.session['movieReservation'] = True
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated '\
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

