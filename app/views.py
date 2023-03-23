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

    return render(request, "website_box_idea/client/signup.html")


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

    return render(request, "website_box_idea/client/signin.html")



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
    return render(request, "website_box_idea/back_office/dashboard.html", {"fname": request.user.first_name})