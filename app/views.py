import re # Package to verify password
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# |-------------------------------||Client views functions||-------------------------------|
def home(request):
    """
    Return to home page view
    """
    return render(request, "website_box_idea/client/home.html")


def signup(request):
    """
    This function allows the user to register to access the various features.
    """

    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm-password"]

        # Check password === confirm_password
        if password != confirm_password:
            messages.error(request, 'Les mots de passe doivent être identiques.')
            return redirect(signup)

        # Check password length, one uppercase, one lowercase, one number and one symbol
        if not re.match("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", password):
            messages.error(request, 'Le mot de passe doit contenir au moins 8 caractères, une lettre majuscule, une lettre minuscule, un chiffre et un symbole.')
            return redirect(signup)

        # Create new user
        try:
            new_user = User.objects.create_user(username, email, password)
            new_user.first_name = fname
            new_user.last_name = lname
            new_user.is_active = True
            new_user.save()
            login(request, new_user)
            messages.success(request, "Votre compte a été créé avec succès.")
            return redirect(signin)
        # If error, return to the sign-up page
        except:
            messages.error(request, "Une erreur est survenue lors de la création de votre compte. Veuillez réessayer plus tard.")
            return redirect(signup)

    return render(request, "coach_Xu_Wenwu_app/client/signup.html")


def signin(request):
    """
    This function allows the user can sign in to access the various features
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(dashboard)

        else:
            messages.error(request, "Nom d'utilisateur et/ou Mot de passe incorrect.")
            return redirect(signin)

    return render(request, "coach_Xu_Wenwu_app/client/signin.html")



def signout(request):
    """
    Function for a correct logout
    """
    logout(request)
    messages.success(request, "Déconnexion réussie.")
    return redirect(home)


@login_required(login_url='/sign-in')
def dashboard(request):
    """
    Function return to the dashboard view
    """
    return render(request, "coach_Xu_Wenwu_app/back_office/dashboard.html", {"fname": request.user.first_name})


@login_required(login_url='/sign-in')
def take_appointment(request):
    """
    Function to access to the take appointment page
    """
    return render(request, "coach_Xu_Wenwu_app/back_office/take_appointment.html")


@login_required(login_url='/sign-in')
def book_appointment(request):
    """
    Function allowing the user to make an appointment
    """
    if request.method == 'POST':
        form = FormPickDate(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            time_slot = form.cleaned_data['time_slot']
            subject = form.cleaned_data['subject']

            # Check if the day is a weekend
            if date.weekday() >= 5:
                messages.error(request, "Vous ne pouvez pas prendre de rendez-vous les week-ends.")
                return redirect(book_appointment)

            # Check to see if the appointment date and time are already set
            existing_appointment = PickDate.objects.filter(date=date, time_slot=time_slot)
            if existing_appointment.exists():
                messages.error(request, 'Ce rendez-vous est déjà pris.')
                return redirect(book_appointment)
            # Saves the data to the database
            appointment = PickDate(
                date=date,
                time_slot=time_slot,
                subject=subject,
                user=request.user,
                name=request.user.first_name + ' ' + request.user.last_name,
                email=request.user.email,
            )

            appointment.save()
            messages.success(request, 'Votre rendez-vous a été pris avec succès!')
            return redirect(book_appointment)
    else:
        form = FormPickDate()

    return render(request, 'coach_Xu_Wenwu_app/back_office/take_appointment.html', {'form': form})



@login_required(login_url='/sign-in')
def view_appointments(request):
    """
    Function that allows the user to see his appointments
    """
    user_appointments_informations = PickDate.objects.filter(user=request.user)
    if request.user.is_staff:
        return render(request, 'coach_Xu_Wenwu_app/back_office/history_appointment.html',
                      {'appointments': user_appointments_informations, 'is_superuser': True})
    else:
        return render(request, 'coach_Xu_Wenwu_app/back_office/history_appointment.html', {'appointments': user_appointments_informations})



# |-------------------------------||Coach views functions||-------------------------------|
@login_required(login_url='/sign-in')
def patient_appointments(request, patient_name):
    """
    Function that gives a different view so that the trainer can see all the patients
    """
    patient_appointments = PickDate.objects.filter(name=patient_name)
    return render(request, 'coach_Xu_Wenwu_app/back_office/history_appointment.html',
                  {'appointments': patient_appointments, 'is_superuser': True})

@login_required(login_url='/sign-in')
def general_appointments_view(request):
    """
    Allows the coach to access a patient's appointments
    """
    patient = PickDate.objects.values('name').distinct()
    return render(request, "coach_Xu_Wenwu_app/back_office/coach_history_appointment.html", {"patients": patient})


@login_required(login_url='/sign-in')
def edit_notes(request, appointment_id):
    """
    Function that allows the coach to put a note in relation to an appointment, not visible by the patient
    """
    appointment = PickDate.objects.get(id=appointment_id)
    if request.method == 'POST':
        form = EditNoteForm(request.POST)
        if form.is_valid():
            appointment.notes = form.cleaned_data['note']
            appointment.save()
            messages.success(request, 'Note modifiée avec succès!')
            return redirect(view_appointments)
    else:
        form = EditNoteForm(initial={'note': appointment.notes})
    return render(request, 'coach_Xu_Wenwu_app/back_office/edit_notes.html', {'form': form})