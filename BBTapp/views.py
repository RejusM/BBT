from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm
from .models import Event


# Pagrindinis puslapis
def home(request):
    events = Event.objects.all()  # Rodo visus renginius
    return render(request, 'home.html', {'events': events})


# Registracija
def register(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Šis metodas tinkamai išsaugo User ir UserProfile
            messages.success(request, "Registracija sėkminga! Dabar galite prisijungti.")
            return redirect('login')
        else:
            messages.error(request, "Patikrinkite formos laukus.")
    else:
        form = UserProfileForm()
    return render(request, 'registration/register.html', {'form': form})


# Vartotojo profilis (tik prisijungusiems vartotojams)
@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})


# Renginio detalės
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})
