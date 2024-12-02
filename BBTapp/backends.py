from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import UserProfile
from django.db.models import Q


class EmailUsernameNicknameBackend(BaseBackend):
    """
    Autentifikavimo backend'as, leidžiantis prisijungti naudojant el. paštą, vartotojo vardą (username) arba slapyvardį (nickname).
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Bandome rasti vartotoją pagal email arba username
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            try:
                # Jei nepavyko, ieškome vartotojo pagal nickname
                user_profile = UserProfile.objects.get(nickname=username)
                user = user_profile.user
            except UserProfile.DoesNotExist:
                return None

        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
