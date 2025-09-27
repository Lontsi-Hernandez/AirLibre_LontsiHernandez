from datetime import datetime
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
from .models import Activity, Category
from django.core.paginator import Paginator
from .detail_activites import get_air_quality
from .form import SignupForm, UserProfileForm
from .form import LoginForm
from .form import LoginForm
from django.contrib.auth.models import User
from . models import Activity
from django.contrib.auth import authenticate,login
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .form import ActivityForm

User = get_user_model()


def index(request):
  
    categorie_id = request.GET.get('categorie')
  
    page_number = request.GET.get('page', 1)

    activities = Activity.objects.all().order_by('start_time')

    if categorie_id:
        activities = activities.filter(category_id=categorie_id)



    paginator = Paginator(activities, 3)
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'activity/index.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_categorie': categorie_id,
      
    })


def signup(request):
    """ Vue pour l'inscription de l'utilisateur """
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])

            
            bio = form.cleaned_data.get('bio')
            if bio:
                user.bio = bio

            user.save()  
            
            messages.success(request, "Inscription réussie ! Vous pouvez maintenant vous connecter.")
            return redirect('connexion')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = SignupForm()

    return render(request, 'activity/signup.html', {'form': form})




def connexion(request):
    """ Vue pour la connexion de l'utilisateur """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=user, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Connexion réussie, Bienvenue {user.first_name}!")
                
                return render(request, 'activity/index.html')

        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = LoginForm()

    return render(request, 'activity/login.html', {"form": form})

@login_required(login_url='connexion')
def profil(request):
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect('profil')
    else:
        form = UserProfileForm(instance=user)

 
    activites_creees = Activity.objects.filter(proposer=user).order_by('-start_time')

    print("Avatar",user.avatar)
    activites_inscriptions = Activity.objects.filter(attendees=user).order_by('-start_time')

    return render(request, "activity/profil.html", {
        "form": form,
        "activites_creees": activites_creees,
        "activites_inscriptions": activites_inscriptions,
    })

@login_required(login_url='login')
def deconnexion(request):
    """ Vue pour la déconnexion de l'utilisateur """
    
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('index')

def toutes_activites(request):
    return redirect('index')

@login_required(login_url='connexion')
def mes_activites(request, id):
    
    activites = Activity.objects.filter(proposer_id=id)
    print(activites)
    return render(request, 'activity/mes_activites.html', {'activites': activites})




@login_required(login_url='connexion')
def s_inscrire(request, id, id_u):
    activity = get_object_or_404(Activity, pk=id)
    print("Activite :",activity)
    user = get_object_or_404(User, pk=id_u) 
    print("User :",user)
     
    activity.attendees.add(user)
    messages.success(request, f"Vous vous êtes inscrit à l'activité '{activity.title}'.")
    return redirect('activity_detail', location_city=activity.location_city, id=activity.id)


@login_required(login_url='connexion')
def se_desinscrire(request, id):
    activity = get_object_or_404(Activity, id=id)
    user = request.user
    activity.attendees.remove(user)
    messages.success(request, f"Vous vous êtes désinscrit de l'activité '{activity.title}'.")
    return redirect('activity_detail', location_city=activity.location_city, id=activity.id)

@login_required(login_url='connexion')    
def mes_inscriptions(request, id):
    
    inscriptions = Activity.objects.filter(attendees=request.user).order_by('start_time')
    page_number = request.GET.get('page', 1)
    paginator = Paginator(inscriptions, 3)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'activity/mes_inscriptions.html', {'page_obj': page_obj})

@login_required(login_url='connexion')
def ajouter_activite(request):
    
    if request.method == "POST":
        form = ActivityForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect("mes_activites", id=request.user.id)
    else:
        form = ActivityForm()
        
    
    return render(request, "activity/form_activity.html", {"form": form})

@login_required(login_url='connexion')
def activity_detail(request, location_city, id):
    activity = get_object_or_404(Activity,id=id, location_city=location_city)
    air_quality = get_air_quality(location_city)
    return render(request, 'activity/activity_detail.html', {
        'activity': activity,
        'air_quality': air_quality,
    })