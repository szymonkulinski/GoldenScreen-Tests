from django import forms

class UserFinalizationForm(forms.Form):
    name = forms.CharField(label='Imię')
    last_name = forms.CharField(label='Nazwisko')
    email = forms.EmailField(label='Adres e-mail')