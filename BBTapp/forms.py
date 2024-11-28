from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from datetime import datetime


class UserProfileForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Slaptažodis",
        widget=forms.PasswordInput,
        help_text="Slaptažodis turi būti bent 8 simbolių ilgio, turėti bent vieną skaičių ir raidę.",
    )
    password2 = forms.CharField(
        label="Pakartokite slaptažodį",
        widget=forms.PasswordInput,
        help_text="Pakartokite slaptažodį.",
    )

    class Meta:
        model = UserProfile
        fields = [
            'nickname', 'first_name', 'last_name', 'email', 'birthdate',
            'gender', 'phone_number', 'country', 'city', 'agrees_to_terms'
        ]
        labels = {
            'nickname': 'Slapyvardis',
            'first_name': 'Vardas',
            'last_name': 'Pavardė',
            'email': 'El. paštas',
            'birthdate': 'Gimimo data',
            'phone_number': 'Telefono numeris',
            'country': 'Šalis',
            'city': 'Miestas',
            'gender': 'Lytis',
            'agrees_to_terms': 'Sutinku su taisyklėmis'
        }
        widgets = {
            'birthdate': forms.DateInput(attrs={'placeholder': 'yyyy-mm-dd', 'type': 'date'})
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Slaptažodžiai nesutampa.")
        validate_password(password1)  # Tikrinama pagal Django saugumo standartus
        return password2

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user = User(
            username=self.cleaned_data['nickname'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
        )
        user.set_password(self.cleaned_data['password1'])  # Slaptažodis užkoduojamas
        user.save()
        user_profile.user = user
        if commit:
            user_profile.save()
        return user_profile

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
            raise ValidationError("Gimimo data negali būti ateities data.")
        return birthdate
