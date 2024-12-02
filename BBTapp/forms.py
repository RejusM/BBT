from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from datetime import datetime


class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(
        label="El. paštas",
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Įveskite el. paštą'}),
        help_text="Slaptažodis turi būti bent 8 simbolių ilgio, turėti bent vieną skaičių ir raidę."
    )
    password1 = forms.CharField(
        label="Slaptažodis",
        widget=forms.PasswordInput(attrs={'placeholder': 'Įveskite slaptažodį'}),
    )
    password2 = forms.CharField(
        label="Pakartokite slaptažodį",
        widget=forms.PasswordInput(attrs={'placeholder': 'Pakartokite slaptažodį'}),
    )

    class Meta:
        model = UserProfile
        fields = [
            'nickname', 'first_name', 'last_name', 'birthdate', 'gender',
            'phone_number', 'country', 'city'
        ]
        labels = {
            'nickname': 'Slapyvardis',
            'first_name': 'Vardas',
            'last_name': 'Pavardė',
            'birthdate': 'Gimimo data',
            'gender': 'Lytis',
            'phone_number': 'Telefono numeris',
            'country': 'Šalis',
            'city': 'Miestas',
        }
        widgets = {
            'birthdate': forms.DateInput(
                attrs={
                    'type': 'date',
                    'placeholder': 'yyyy-mm-dd',
                },
                format='%Y-%m-%d'
            ),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Slaptažodžiai nesutampa.")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Šis el. paštas jau užregistruotas.")
        return email

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if UserProfile.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError("Šis slapyvardis jau užregistruotas.")
        return nickname

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate > datetime.today().date():
            raise forms.ValidationError("Gimimo data negali būti ateities data.")
        return birthdate

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = User(
            username=self.cleaned_data['nickname'],  # Slapyvardis kaip username
            email=self.cleaned_data['email'],  # El. pašto saugojimas
        )
        user.set_password(self.cleaned_data['password1'])  # Užšifruokite slaptažodį
        if commit:
            user.save()
            profile.user = user  # Priskirkite vartotoją UserProfile
            profile.save()
        return profile
