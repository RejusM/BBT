from django.shortcuts import render, redirect
from .forms import UserProfileForm
from django.contrib import messages
from django.contrib.auth import get_user_model


def home(request):
    return render(request, 'home.html')  # Pagrindinis puslapis


def register(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Išsaugome vartotoją
            user = form.save()
            messages.success(request, "Registracija sėkminga!")

            # El. laiško siuntimas (užkomentuotas)
            # send_mail(
            #     'Sėkminga registracija',
            #     'Sveikiname prisijungus prie mūsų sistemos!',
            #     'admin@jusu-sistema.lt',
            #     [form.cleaned_data.get('email')],
            #     fail_silently=False,
            # )

            return redirect('login')
        else:
            messages.error(request, "Patikrinkite formos laukus.")
    else:
        form = UserProfileForm()

    return render(request, 'registration/register.html', {'form': form})
