from django import forms
from .models import Temoin
from .models import Article
from .models import Reservation
from .models import Formation
from .models import  MessageContact  
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm
from .models import Inscription
from .models import Inscription, MODE_CHOICES, TRIMESTRE_CHOICES

class TemoinForm(forms.ModelForm):
    class Meta:
        model = Temoin
        fields = ['nom', 'commentaire']  # 👈 statut

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'image', 'auteur', 'categorie'] 


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["nom", "email", "date", "objet"]
        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }



class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['titre', 'description', 'objet', 'date_debut', 'date_fin', 'prix','trimestre', 'lieu', 'horaire', 'mode', 'image', 'publie', 'duree']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
            'horaire': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ex : Lundi 7h-12h, Mercredi 14h-17h'}),
            'mode': forms.Select(attrs={'class': 'form-select'}),
            'duree': forms.TextInput(attrs={'placeholder': 'Ex : 3 mois'}),
            'trimestre': forms.Select(attrs={'class': 'form-select'}),
        }
class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ['nom', 'email', 'telephone', 'mode', 'trimestre']

class MessageForm(forms.ModelForm):
    class Meta:
        model = MessageContact
        # ne garder que les champs existants dans ton modèle
        fields = ['nom', 'email', 'sujet', 'type_demande', 'message', 'cv']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
            'sujet': forms.TextInput(attrs={'placeholder': 'Objet du message'}),
        }




class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'bio']


        

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Mot de passe'
    }))


class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ["nom", "email", "telephone"]