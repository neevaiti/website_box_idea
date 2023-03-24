import re # Package to verify password
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404


from .models import Idea, Comment
from .forms import IdeaForm, CommentForm



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
            messages.error(request, "Pseudo et/ou Mot de passe incorrect.")
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
    messages.success(request, f"Bienvenue {request.user.first_name} sur votre tableau de bord.")
    
    return render(request, "website_box_idea/back_office/dashboard.html", {"fname": request.user.first_name})


@login_required(login_url='/sign-in')
def ideas_list(request):
    idees = Idea.objects.all()
    return render(request, 'website_box_idea/back_office/display_ideas.html', {'ideas': idees})


@login_required(login_url='/sign-in')
def new_idea(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        #author = request.POST['author']
        #created_at = request.POST['created_at']
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            
            post_idea = Idea(
                title=title,
                description=description,
                author=request.user,
            )
            #new_idea.created_at = request.created_at
            post_idea.save()
            messages.success(request, "Votre idée a été publiée!")
            return redirect(ideas_list)
    else:
        form = IdeaForm()
    return render(request, 'website_box_idea/back_office/new_ideas.html', {'form': form})


@login_required(login_url='/sign-in')
def new_comment(request, idea_id):
    idea = get_object_or_404(Idea, pk=idea_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            commentary = form.save(commit=False)
            commentary.author = request.user
            commentary.idea = idea
            commentary.save()
            messages.success(request, "Votre commentaire a été publié!")
            return redirect('idees_list')
    else:
        form = CommentForm()
    return render(request, 'boite_a_idees/new_comment.html', {'form': form})


@login_required(login_url='/sign-in')
def like_idea(request):
    if request.method == 'POST' and request.is_ajax():
        idea_id = request.POST.get('idea_id')
        idea = get_object_or_404(Idea, id=idea_id)
        idea.likes += 1
        idea.save()
        data = {'success': True, 'likes': idea.likes}
        return JsonResponse(data)
    else:
        data = {'success': False}
        return JsonResponse(data)


@login_required(login_url='/sign-in')
def like_comment(request):
    if request.method == 'POST' and request.is_ajax():
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)
        comment.likes += 1
        comment.save()
        data = {'success': True, 'likes': comment.likes}
        return JsonResponse(data)
    else:
        data = {'success': False}
        return JsonResponse(data)


@login_required(login_url='/sign-in')
def dislike_idea(request):
    if request.method == 'POST' and request.is_ajax():
        idea_id = request.POST.get('idea_id')
        idea = get_object_or_404(Idea, id=idea_id)
        idea.dislikes += 1
        idea.save()
        data = {'success': True, 'dislikes': idea.dislikes}
        return JsonResponse(data)
    else:
        data = {'success': False}
        return JsonResponse(data)


@login_required(login_url='/sign-in')
def dislike_comment(request):
    if request.method == 'POST' and request.is_ajax():
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)
        comment.dislikes += 1
        comment.save()
        data = {'success': True, 'dislikes': comment.dislikes}
        return JsonResponse(data)
    else:
        data = {'success': False}
        return JsonResponse(data)