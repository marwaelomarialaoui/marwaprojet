from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages as django_messages
from django.views.decorators.http import  require_POST  # <-- Ajout 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .forms import ArticleForm, TemoinForm ,ReservationForm , FormationForm  
from django.contrib.auth import get_user_model


from django import forms


from alexsys_site.home.models import MessageContact





from .models import Profile,  ReservationClient, Article, Temoin
from django.dispatch import receiver
from .forms import ProfileForm ,LoginForm
from .models import Reponse , Formation,Inscription , Paiement

from .forms import InscriptionForm
import json

from django.db.models.signals import post_save
from django.contrib.auth.models import User




from .models import MessageContact, Temoin, Article ,Reservation , Formation
 
 # -------------------- Accueil -------------------

def index(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        type_demande = request.POST.get('type_demande')
        message = request.POST.get('message')
        cv = request.FILES.get('cv')  # fichier uploadé

        if nom and email and sujet and type_demande and message:
            # Sauvegarder en base, avec fichier CV si modèle gère le fichier
            # Exemple si tu as un champ FileField dans MessageContact pour cv:
            contact_msg = MessageContact(
                nom=nom,
                email=email,
                sujet=sujet,
                type_demande=type_demande,
                message=message,
                cv=cv  # à condition que ton modèle ait ce champ
            )
            contact_msg.save()

            django_messages.success(request, "Merci, votre message a bien été envoyé !")
            return redirect('index')
        else:
            django_messages.error(request, "Merci de remplir tous les champs obligatoires.")

    return render(request, 'home/index.html')



# -------------------- Témoignages --------------------

# ✅ Client ajoute témoignage
# Client ajoute témoignage
def ajouter_temoin(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        commentaire = request.POST.get('commentaire')
        note = request.POST.get('note', 5)  # par défaut 5 si rien
        if nom and commentaire:
            Temoin.objects.create(nom=nom, commentaire=commentaire, note=note)
    return redirect('temoins')

# Frontend - afficher que acceptés
def temoins(request):
    temoins = Temoin.objects.filter(statut='accepte').order_by('-date')
    return render(request, 'temoins.html', {'temoins': temoins})

# Admin - gérer témoignages directement, sans login
def gerer_temoins(request):
    temoins = Temoin.objects.filter(statut='en_attente').order_by('-date')
    return render(request, 'home/gere_temoins.html', {'temoins': temoins})

def accepter_temoin(request, temoin_id):
    tem = get_object_or_404(Temoin, id=temoin_id)
    tem.statut = 'accepte'
    tem.save()
    return redirect('gerer_temoins')

def refuser_temoin(request, temoin_id):
    tem = get_object_or_404(Temoin, id=temoin_id)
    tem.statut = 'refuse'
    tem.save()
    return redirect('gerer_temoins')






def admin_panel(request):
    temoins = Temoin.objects.all()
    messages = MessageContact.objects.all().order_by('-date_envoi')
    return render(request, 'home/admin_panel.html', {
        'temoins': temoins,
        'messages': messages
    })
def dashboard(request):
    return render(request, 'home/dashboard.html')

def a_propos(request):
    return render(request, 'home/a_propos.html')

# Page publique des témoignages (seulement acceptés)
def temoins(request):
    temoins = Temoin.objects.filter(statut='accepte').order_by('-date')
    return render(request, 'home/temoins.html', {'temoins': temoins})



# -------------------- Messages --------------------
# -------------------- Contact --------------------
def contact(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')
        MessageContact.objects.create(
            nom=nom,
            email=email,
            sujet=sujet,
            message=message,
            statut="en_attente"
        )
        django_messages.success(request, "Votre message a été envoyé !")
        return redirect('contact')
    return render(request, 'home/contact.html')

# -------------------- Liste Messages Admin ---------------
def messages_contact(request):
    messages_list = MessageContact.objects.all().order_by('-date_envoi')
    return render(request, 'home/messages_contact.html', {'messages': messages_list})
@require_POST
def accepter_message(request, id):
    msg = get_object_or_404(MessageContact, id=id)
    msg.statut = 'accepte'
    msg.save()
    return redirect('messages_contact')

@require_POST
def refuser_message(request, id):
    msg = get_object_or_404(MessageContact, id=id)
    msg.statut = 'refuse'
    msg.save()
    return redirect('messages_contact')
# -------------------- Envoyer Réponse Admin --------------------






def envoyer_reponse(request, id):
    # Récupérer le message de contact
    msg = get_object_or_404(MessageContact, id=id)

    if request.method == 'POST':
        corps = request.POST.get('corps')

        if corps:
            # ➕ نحفظ الرد داخل نفس modèle
            msg.reponse_admin = corps
            msg.statut = "accepte"  # مثلا نعتمد أنه تقبل
            msg.save()

            # ✉️ Envoi email au user
            try:
                send_mail(
                    subject=f"Réponse à votre message: {msg.sujet}",
                    message=corps,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[msg.email],
                    fail_silently=False,
                )
                django_messages.success(request, f"Réponse envoyée à {msg.email}.")
            except Exception as e:
                django_messages.error(request, f"Erreur lors de l'envoi: {e}")

            return redirect('messages_contact')
        else:
            django_messages.error(request, "Le message est obligatoire.")

    return render(request, 'home/envoyer_reponse.html', {'message': msg})


# -------------------- Messages User --------------------
def mes_messages(request):
    messages_user = []

    # Si l'utilisateur a fourni son email dans GET ou POST
    email = request.GET.get('email') or request.POST.get('email')
    if email:
        # On récupère tous les messages envoyés par cet email
       messages_user = MessageContact.objects.filter(email=email)



    return render(request, 'home/mes_messages.html', {
        'messages_user': messages_user,
        'email': email,
    })












def supprimer_message(request, id):
    msg = get_object_or_404(MessageContact, id=id)
    msg.delete()
    django_messages.success(request, f'Message supprimé.')
    return redirect('messages_contact')


def gerer_formations(request):
    # Ajoute ici la logique que tu souhaites, par exemple :
    return render(request, 'home/gerer_formations.html')


def changer_statut_message(request, message_id):
    msg = get_object_or_404(MessageContact, id=message_id)
    if request.method == "POST":
        statut = request.POST.get("statut")
        if statut in ["accepte", "refuse"]:
            msg.statut = statut
            msg.save()
    return redirect('admin_panel')

def changer_statut_temoin(request, temoin_id, nouveau_statut):
    temoin = get_object_or_404(Temoin, id=temoin_id)
    temoin.statut = nouveau_statut
    temoin.save()
    return redirect('gerer_temoins')

def nos_solutions(request):
    return render(request, 'home/nos_solutions.html')



# -------------------- Articles --------------------

def blog_list(request):
    articles = Article.objects.all().order_by('-date_pub')
    return render(request, 'home/blog_list.html', {'articles': articles})

def blog_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    # ➕ Incrémenter vues
    article.vues = article.vues + 1 if article.vues else 1
    article.save(update_fields=['vues'])
    return render(request, 'home/blog_detail.html', {'article': article})

def gerer_blog(request):
    articles = Article.objects.all().order_by('-date_pub')

   # Incrémenter toutes les vues (attention, chaque reload va ajouter +1 à tous)
    for article in articles:
        article.vues = article.vues + 1 if article.vues else 1
        article.save(update_fields=["vues"])
    
    return render(request, 'home/gerer_blog.html', {'articles': articles})

def ajouter_article(request):
    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect wella affichage après l’ajout
    return render(request, 'home/ajouter_article.html', {'form': form})


# Modifier article
def modifier_article(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('gerer_blog')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'home/modifier_article.html', {'form': form, 'article': article})


# Supprimer article
def supprimer_article(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == 'POST':  # confirmation avant suppression
        article.delete()
        return redirect('gerer_blog')
    return render(request, 'home/confirmer_suppression.html', {'article': article})

 # -------------------- Réservations --------------------
def reserver(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()

            # Envoi notification admin (optionnel)
            send_mail(
                "Nouvelle réservation",
                f"Une nouvelle réservation a été faite par {reservation.nom} ({reservation.email})\nObjet: {reservation.objet}\nDate: {reservation.date}",
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
            )

            return redirect("reservation_success")
    else:
        form = ReservationForm()
    return render(request, "home/reservation_form.html", {"form": form})


def reservation_success(request):
    return render(request, "home/reservation_success.html")


# Vue pour la liste des réservations côté admin
def reservations_list(request):
    # Filtre par statut si fourni via GET
    statut_filtre = request.GET.get('statut')
    if statut_filtre in ['pending', 'accepted', 'rejected']:
        reservations = Reservation.objects.filter(status=statut_filtre).order_by('-created_at')
    else:
        reservations = Reservation.objects.all().order_by('-created_at')
    return render(request, 'home/reservations_list.html', {'reservations': reservations, 'statut_filtre': statut_filtre})

def gerer_reservations(request):
    statut_filtre = request.GET.get('statut')
    if statut_filtre in ['pending', 'accepted', 'rejected']:
        reservations = Reservation.objects.filter(status=statut_filtre).order_by('-created_at')
    else:
        reservations = Reservation.objects.all().order_by('-created_at')
    return render(request, 'home/reservations_list.html', {'reservations': reservations, 'statut_filtre': statut_filtre})

# Vue pour changer le statut d'une réservation
def update_reservation_status(request, pk, status):
    reservation = get_object_or_404(Reservation, pk=pk)
    old_status = reservation.status
    reservation.status = status
    reservation.save()

    # Message par défaut
    client_message = f"Le statut de votre réservation est {reservation.status}."

    if old_status != status:
        if status == "accepted":
            send_mail(
                "Votre réservation est acceptée",
                f"Bonjour {reservation.nom},\n\nVotre réservation pour le {reservation.date} a été acceptée ✅.",
                settings.DEFAULT_FROM_EMAIL,
                [reservation.email],
                fail_silently=False
            )
            client_message = "Votre réservation a été acceptée ✅"
        elif status == "rejected":
            send_mail(
                "Votre réservation est refusée",
                f"Bonjour {reservation.nom},\n\nDésolé, votre réservation pour le {reservation.date} a été refusée ❌.",
                settings.DEFAULT_FROM_EMAIL,
                [reservation.email],
                fail_silently=False
            )
            client_message = "Votre réservation a été refusée ❌"

    # Message côté admin
    django_messages.success(request, f"Le statut de la réservation de {reservation.nom} a été mis à jour.")

    # Page côté client
    return render(request, "home/reservation_status_client.html", {"reservation": reservation, "message": client_message})



# Vue côté client pour créer une réservation
def create_reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'home/reservation_success.html')
    else:
        form = ReservationForm()
    return render(request, 'home/create_reservation.html', {'form': form})



# Modifier une réservation côté admin
def reservation_edit(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            django_messages.success(request, f"Réservation de {reservation.nom} modifiée avec succès.")
            return redirect('reservations_list')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, "home/reservation_form.html", {"form": form})


# Accepter directement depuis admin (shortcut)
def reservation_accept(request, pk):
    return update_reservation_status(request, pk, "accepted")

# Refuser directement depuis admin (shortcut)
def reservation_decline(request, pk):
    return update_reservation_status(request, pk, "rejected")


# views.py
def reservation_client_detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "accept":
            reservation.status = "accepted"
            reservation.save()
            client_message = "Votre réservation a été acceptée ✅"
        elif action == "reject":
            reservation.status = "rejected"
            reservation.save()
            client_message = "Votre réservation a été refusée ❌"
        else:
            client_message = "Action inconnue."
        return render(request, "home/reservation_status_client.html", {"reservation": reservation, "message": client_message})

    return render(request, "home/reservation_status_client.html", {"reservation": reservation, "message": ""})

def reservations_client_list(request):
    reservations = Reservation.objects.all().order_by('-created_at')  # filtre selon utilisateur si besoin

    # Gestion du POST pour accepter/refuser
    if request.method == "POST":
        reservation_id = request.POST.get("reservation_id")
        action = request.POST.get("action")
        reservation = get_object_or_404(Reservation, pk=reservation_id)

        if action == "accept":
            reservation.status = "accepted"
            reservation.message = "Votre réservation a été acceptée ✅"
            reservation.save()
        elif action == "reject":
            reservation.status = "rejected"
            reservation.message = "Votre réservation a été refusée ❌"
            reservation.save()

    return render(request, 'home/reservations_client_list.html', {'reservations': reservations})



def reservations_client_list(request):
    code_correct = "1234"  # ton code secret
    message_erreur = ""

    if request.method == "POST":
        code = request.POST.get("code")
        if code == code_correct:
            reservations = Reservation.objects.all().order_by('-created_at')  # filtre selon utilisateur si besoin
            return render(request, 'home/reservations_client_list.html', {'reservations': reservations})
        else:
            message_erreur = "Code incorrect, veuillez réessayer."

    return render(request, 'home/reservations_client_code.html', {"message_erreur": message_erreur})

# Code secret pour accéder aux réservations
SECRET_CODE = "1234"  # tu peux changer ce code



def client_dashboard(request):
    if not request.session.get('code_valid'):
         return render(request, 'home/mes_reservations.html')

    # récupérer tous les messages (ou filtrer selon besoin)
    messages_client = MessageContact.objects.all().order_by('-date_envoi')
    return render(request, 'home/mes_reservations.html', {'messages_contact': messages_client})





# -------------------- Formations --------------------

def gerer_formations(request):
    formations = Formation.objects.all()
    return render(request, 'home/gerer_formations.html', {'formations': formations})

def ajouter_formation(request):
    if request.method == "POST":
        form = FormationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            django_messages.success(request, "Formation ajoutée avec succès !")
            return redirect('gerer_formations')
    else:
        form = FormationForm()
    return render(request, 'home/ajouter_formation.html', {'form': form})
        
def modifier_formation(request, id):
    formation = get_object_or_404(Formation, id=id)
    if request.method == "POST":
        form = FormationForm(request.POST, request.FILES, instance=formation)
        if form.is_valid():
            form.save()
            django_messages.success(request, "Formation modifiée avec succès !")
            return redirect('gerer_formations')
    else:
        form = FormationForm(instance=formation)
    return render(request, 'home/modifier_formation.html', {'form': form})


def supprimer_formation(request, id):
    formation = get_object_or_404(Formation, id=id)
    formation.delete()
    django_messages.success(request, "Formation ajoutée avec succès !")
    return redirect('gerer_formations')



def liste_formations(request):
    # On ne montre que les formations publiées
    formations = Formation.objects.filter(publie=True)
    return render(request, 'home/liste_formations.html', {'formations': formations})

def detail_formation(request, pk):
    formation = Formation.objects.get(pk=pk, publie=True)
    return render(request, 'home/detail_formation.html', {'formation': formation})

# Inscription
def inscription_formation(request, formation_id):
    formation = get_object_or_404(Formation, id=formation_id)

    # Modes disponibles
    if formation.mode == 'mixte':
        modes_disponibles = [('presentiel','Présentiel'), ('en_ligne','En ligne')]
    else:
        modes_disponibles = [(formation.mode, formation.get_mode_display())]

    # Trimestres disponibles
    if formation.trimestre == 'mixte':
        trimestres_disponibles = [
            ('1er','1er trimestre : septembre - novembre'),
            ('2eme','2ème trimestre : décembre - février'),
            ('3eme','3ème trimestre : mars - mai'),
            ('4eme','4ème trimestre : juin - août'),
        ]
    else:
        trimestres_disponibles = [(formation.trimestre, formation.get_trimestre_display())]

    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            inscription = form.save(commit=False)
            inscription.formation = formation

            # 🔹 Récupérer les choix du client depuis le POST
            inscription.mode = request.POST.get('mode')
            inscription.trimestre = request.POST.get('trimestre')

            inscription.save()
            return redirect('mes_inscriptions')
    else:
        form = InscriptionForm()

    return render(request, "home/inscription.html", {
        "formation": formation,
        "form": form,
        "modes_disponibles": modes_disponibles,
        "trimestres_disponibles": trimestres_disponibles
    })


def gerer_inscriptions(request):
    inscriptions = Inscription.objects.all().order_by('-id')
    return render(request, 'home/gerer_inscriptions.html', {'inscriptions': inscriptions})

# Accepter ou refuser une inscription
def update_inscription_status(request, pk, status):
    inscription = get_object_or_404(Inscription, pk=pk)
    inscription.statut = status
    inscription.save()
    return redirect('gerer_inscriptions')

def accepter_inscription(request, insc_id):
    insc = get_object_or_404(Inscription, id=insc_id)
    insc.statut = 'valide'    # doit correspondre au choix "valide"
    insc.save()
    return redirect('gerer_inscriptions')

def refuser_inscription(request, insc_id):
    insc = get_object_or_404(Inscription, id=insc_id)
    insc.statut = 'refuse'    # doit correspondre au choix "refuse"
    insc.save()
    return redirect('gerer_inscriptions')


def mes_inscriptions(request):
    # On récupère toutes les inscriptions, triées par date d'inscription
    inscriptions = Inscription.objects.all().order_by('-date_inscription')
    
    return render(request, 'home/mes_inscriptions.html', {'inscriptions': inscriptions})


def choisir_paiement(request, inscription_id):
    inscription = get_object_or_404(Inscription, id=inscription_id)

    if request.method == "POST":
        prenom = request.POST.get("prenom")
        nom = request.POST.get("nom")
        mode = request.POST.get("mode_paiement")

        service = ""
        details = {}

        if mode == "online":
            service = request.POST.get("online_service")
            if service in ["carte", "bp"]:
                details = {
                    "numero": request.POST.get("numero"),
                    "expiration": request.POST.get("expiration"),
                    "cvv": request.POST.get("cvv"),
                    "rue": request.POST.get("rue"),
                    "code_postal": request.POST.get("code_postal"),
                    "ville": request.POST.get("ville"),
                    "pays_region": request.POST.get("pays_region"),
                    "titulaire_carte": request.POST.get("titulaire_carte"),
                }
            elif service == "paypal":
                details = {"paypal_email": request.POST.get("paypal_email")}

        elif mode == "mobile":
            service = request.POST.get("mobile_service")
            details = {
                "tel_mobile": request.POST.get("tel_mobile"),
                "montant": request.POST.get("montant"),
                "reference": request.POST.get("reference"),
            }

        elif mode == "classique":
            service = request.POST.get("classique_service")
            if service == "virement":
                details = {"rib": request.POST.get("rib")}
            # pour espèces et chèque, details reste vide

        # Si tu utilises TextField, convertir en JSON
        Paiement.objects.create(
            inscription=inscription,
            prenom=prenom,
            nom=nom,
            mode_paiement=mode,
            service=service,
            details=json.dumps(details) if not isinstance(details, str) else details,
            statut="Validé"
        )

        inscription.paye = True
        inscription.save()

        django_messages.success(request, f"✅ Paiement de {prenom} {nom} validé avec succès !")
        return redirect("choisir_paiement", inscription.id)

    return render(request, "home/choisir_paiement.html", {"inscription": inscription})

def gerer_paiements(request):
    statut = request.GET.get('statut', 'tous')  # récupère le statut depuis le GET
    if statut == 'tous':
        inscriptions = Inscription.objects.all()
    else:
        # correspondance avec les valeurs de la base
        mapping = {
            'En attente': 'en_attente',
            'Validé': 'valide',
            'Refusé': 'refuse'
        }
        inscriptions = Inscription.objects.filter(statut=mapping.get(statut, 'en_attente'))

    context = {
        'inscriptions': inscriptions,
        'filtre_statut': statut
    }
    return render(request, 'home/gerer_paiements.html', context)


def valider_paiement(request, inscription_id):
    inscription = Inscription.objects.get(id=inscription_id)
    inscription.paiement_effectue = True
    inscription.statut = 'valide'
    inscription.save()

    # Message succès
    django_messages.success(request, f"✅ Paiement de {inscription.nom} validé avec succès !")

    return redirect('gerer_paiements')




def confirmer_paiement(request, id):
    inscription = get_object_or_404(Inscription, id=id)

    if request.method == "POST":
        prenom = request.POST.get("prenom")
        nom = request.POST.get("nom")
        email = request.POST.get("email")
        telephone = request.POST.get("telephone")
        adresse = request.POST.get("adresse")
        mode = request.POST.get("mode_paiement")

        # tu enregistres le paiement
        Paiement.objects.create(
            inscription=inscription,
            prenom=prenom,
            nom=nom,
            email=email,
            telephone=telephone,
            adresse=adresse,
            mode_paiement=mode,
            statut="en attente",  # par exemple
        )

        django_messages.success(request, "✅ Paiement envoyé, en attente de validation par l’administration.")
        return redirect("mes_inscriptions")

    return render(request, "home/choisir_paiement.html", {"inscription": inscription})

def gestion_paiements(request):
    inscriptions = Inscription.objects.all()
    return render(request, 'home/gestion_paiements.html', {'inscriptions': inscriptions})




# -------------------dashboard côté client---------------------------




@login_required(login_url="user_login")
def dashboard(request):
    # récupère le profil unique
    profile = Profile.objects.first()  # puisque tu n'as qu'un seul profil
    return render(request, 'home/dashboard.html', {'profile': profile})

@login_required
def detail_reservation(request, id):
    res = get_object_or_404(ReservationClient, id=id, client=request.user)
    return render(request, 'home/detail_reservation.html', {'reservation': res})

def annuler_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        reservation.delete()
        django_messages.success(request, "Réservation annulée avec succès ✅")
        return redirect('reservations_list')
    except Reservation.DoesNotExist:
        django_messages.error(request, "Cette réservation n'existe pas.")
        return redirect('reservations_list')

@login_required
def detail_message(request, id):
    msg = get_object_or_404(MessageContact, id=id, client=request.user)
    return render(request, 'home/detail_message.html', {'message': msg})

@login_required
def nouvelle_reservation(request):
    # Formulaire de création ici (à adapter selon ton projet)
    pass



def modifier_profil(request):
    profile, created = Profile.objects.get_or_create(id=1)  # 1 seul profil
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('modifier_profil')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'home/modifier_profil.html', {'form': form, 'profile': profile})

User = get_user_model()
# Page de connexion
def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            django_messages.error(request, "Email ou mot de passe invalide.")

    return render(request, 'login.html')

# Dashboard protégé
@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'dashboard.html')  # dashboard.html dans templates/


# Code secret pour accéder au panel admin custom
SECRET_CODE = "2004"  # 🔑 change-le comme tu veux

def admin_panel_code(request):
    """
    Page qui demande le code secret avant d'accéder à l'admin panel custom.
    """
    message_erreur = ""

    if request.method == "POST":
        code = request.POST.get("code")
        if code == SECRET_CODE:
            # Stocker en session que le code a été validé
            request.session['admin_authenticated'] = True
            return redirect('admin_panel')  # redirige vers la vraie page admin
        else:
            message_erreur = "❌ Code incorrect, veuillez réessayer."

    return render(request, 'home/admin_panel_code.html', {"message_erreur": message_erreur})


# Code secret pour accéder au panel admin
SECRET_CODE = "2004"  # 🔑 change-le comme tu veux

def admin_panel(request):
    """
    Page admin protégée par code secret : demande le code à chaque accès
    """
    message_erreur = ""

    if request.method == "POST":
        code = request.POST.get("code")
        if code == SECRET_CODE:
            return render(request, "home/admin_panel.html")  # accès autorisé
        else:
            message_erreur = "❌ Code incorrect, veuillez réessayer."

    # Si GET ou mauvais code -> afficher formulaire code
    return render(request, "home/admin_panel_code.html", {"message_erreur": message_erreur})


def user_login(request):
    if request.user.is_authenticated:
        # si user deja connecté, redirect direct dashboard
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "❌ Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, "home/login.html")

def user_logout(request):
    logout(request)
    return redirect("user_login")