from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate

class LoginForm(forms.ModelForm):
    username = forms.CharField(label='Nazwa użytkownika')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password']
	    
        labels = {
	    'username' : 'Nazwa użytkownika',
	    'password' : 'Hasło',
		}
    
class ChangeEmailForm(forms.Form):
    email1 = forms.EmailField(label='Nowy adres email',
                              widget=forms.EmailInput,)
    email2 = forms.EmailField(label='Potwierdź adres email',
                              widget=forms.EmailInput,)
    password = forms.CharField(label='Hasło',
                               widget=forms.PasswordInput)
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangeEmailForm, self).__init__(*args, **kwargs)

    def clean_email1(self):
        old_email = self.user.email
        email1 = self.cleaned_data.get('email1')
        if old_email and email1:
            if old_email == email1:
                raise forms.ValidationError('Nowy adres email musi się różnić od poprzedniego.')
        return email1
    
    def clean_email2(self):
        email1 = self.cleaned_data.get('email1')
        email2 = self.cleaned_data.get('email2')
        if email1 and email2:
            if email1 != email2:
                raise forms.ValidationError('Podane adresy muszą być takie same.')
        return email2

    def save(self, commit=True):
        email = self.cleaned_data["email1"]
        self.user.email = email
        if commit:
            self.user.save()
        return self.user

class DeactivateForm(forms.ModelForm):
    password = forms.CharField(label='Hasło',
                               widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['password']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Hasło',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło',
                                widget=forms.PasswordInput)
    username = forms.CharField(label='Nazwa użytkownika')
    email = forms.EmailField(label='Adres e-mail')

    class Meta:
        model = User
        fields = ('username', 'email')
		
        labels = {
	    'username' : 'Nazwa użytkownika',
	    'email' : 'Adres e-mail',
		}
        
    def clean_password2(self):
        cd = self.cleaned_data
        if 'password' in cd.keys():
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Hasła nie pasują do siebie.')
            if len(cd['password']) < 8:
                raise forms.ValidationError('Hasło powinno mieć conajmniej 8 znaków.')
            return cd['password2']
        else:
            raise forms.ValidationError('To pole jest wymagane.')
		
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'email']:
            self.fields[fieldname].help_text = None
            
