from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, unique=True)
    birthdate = models.DateField(help_text="Įveskite gimimo datą (YYYY-MM-DD)")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    country = CountryField(default='LT')
    city = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(
        upload_to='profile_photos/',
        default='profile_photos/default-user.png',  # Numatytoji nuotrauka
        blank=True
    )
    gender = models.CharField(
        max_length=1,
        choices=[('V', 'Vyras'), ('M', 'Moteris')],
        blank=False,
        null=False
    )
    agrees_to_terms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nickname} ({self.first_name} {self.last_name})"


# Etapas (renginys, vyksta tam tikrą dieną ir vietą)
class Event(models.Model):
    name = models.CharField(max_length=100)  # Pvz.: Kauno etapas
    location = models.CharField(max_length=100)  # Pvz.: Kaunas
    date = models.DateField()  # Kada vyks etapas
    description = models.TextField(blank=True, null=True)  # Aprašymas

    def __str__(self):
        return f"{self.name} ({self.date})"


# Trasa (susijusi su konkrečiu etapu)
class Track(models.Model):
    GENDER_CHOICES = [
        ('V', 'Vyrai'),
        ('M', 'Moterys'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tracks")
    name = models.CharField(max_length=50)  # Pvz.: 10km arba 5km
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    price = models.DecimalField(max_digits=5, decimal_places=2)  # Pradinė kaina
    late_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Kaina po brangimo datos
    late_price_date = models.DateField(blank=True, null=True)  # Brangimo data

    def __str__(self):
        return f"{self.event.name} - {self.name} ({self.price}€)"


# Dalyvis (registracija į trasą)
class Registration(models.Model):
    GENDER_CHOICES = [
        ('V', 'Vyrai'),
        ('M', 'Moterys'),
    ]

    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)  # Pasirinkta trasa
    email = models.EmailField()
    agreed_to_terms = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} {self.surname} - {self.track}"
