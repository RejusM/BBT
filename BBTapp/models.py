from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
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
