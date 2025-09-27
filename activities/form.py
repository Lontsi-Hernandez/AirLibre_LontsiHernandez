from django import forms
from .models import Activity, User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm


        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-contro'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        
class SignupForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), label="Prénom",error_messages={'required': 'Le prénom est obligatoire.'})
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), label="Nom",error_messages={'required': 'Le nom est obligatoire.'})
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label="Email",error_messages={'required': 'L\'email est obligatoire.', 'invalid': 'Veuillez entrer une adresse email valide.'})
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}), label="Nom d'utilisateur",error_messages={'required': 'Le nom d\'utilisateur est obligatoire.'})
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}), label="Avatar")
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False, label="Bio")

    class Meta:
        model = User
        fields = ['username', 'email', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom d’utilisateur'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse courriel'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
        }
        labels = {
            'username': 'Nom d’utilisateur',
            'email': 'Adresse courriel',
            'avatar': 'Photo de profil',
        }
        help_texts = {
            'username': 'Choisissez un nom unique pour vous connecter.',
            'email': 'Nous utiliserons cette adresse pour vous contacter.',
            'avatar': 'Téléversez une image',
        }


    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

   


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=150)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Nom d'utilisateur ou mot de passe incorrect.")
            self.user = user
        return cleaned_data

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            "title",
            "description",
            "location_city",
            "start_time",
            "end_time",
            "proposer",
            "attendees",
            "category",
            "created_by",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Titre"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "location_city": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ville"}),
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "proposer": forms.Select(attrs={"class": "form-control"}),
            "attendees": forms.SelectMultiple(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "created_by": forms.Select(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and end_time <= start_time:
            raise ValidationError("La date de fin doit être après la date de début.")
        
        return cleaned_data

    