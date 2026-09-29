from django.db import models
from django.contrib.auth.models import User   # Pour le lien avec le client
from django.utils import timezone
from django.db.models import JSONField
 # si PostgreSQL

# ---------------------------------------------
# Témoins
# ---------------------------------------------

# home/models.py


class Temoin(models.Model):
    nom = models.CharField(max_length=200)
    commentaire = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    
    # statut : en_attente / accepte / refuse
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('accepte', 'Accepté'),
        ('refuse', 'Refusé'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
 
# Ajouter la note
    note = models.PositiveSmallIntegerField(default=5)

    def __str__(self):
        return f"{self.nom} - {self.statut} - {self.note}★"


# ---------------------------------------------
# Messages de contact
# ---------------------------------------------

class MessageContact(models.Model):
    TYPE_CHOICES = [
        ('contact', 'Message de contact'),
        ('stage', 'Demande de stage'),
        ('cv', 'Envoi de CV'),
    ]
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('accepte', 'Accepté'),
        ('refuse', 'Refusé'),
    ]
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    sujet = models.CharField(max_length=200)
    message = models.TextField()
    type_demande = models.CharField(max_length=20, choices=TYPE_CHOICES, default='contact')
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)
    date_envoi = models.DateTimeField(auto_now_add=True)  # <-- corrige ici
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    
     # ➕ هادي هي اللي غادي تخلي الرد يتخزن
    reponse_admin = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.nom} - {self.sujet}"

# ---------------------------------------------
# Articles
# ---------------------------------------------

class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    date_pub = models.DateTimeField(auto_now_add=True)
    auteur = models.CharField(max_length=100, blank=True, null=True)
    categorie = models.CharField(max_length=100, blank=True, null=True)
    vues = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titre
    
class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="articles/")

    def __str__(self):
        return f"Image de {self.article.titre}"
      



class Reservation(models.Model):
    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("accepted", "Acceptée"),
        ("rejected", "Rejetée"),
    ]

    nom = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateTimeField()
    objet = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.date.strftime('%d/%m/%Y %H:%M')}"
      
# ---------------------------------------------
# Formations
# ---------------------------------------------
class Formation(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    objet = models.CharField(max_length=200, blank=True, null=True)  
    date_debut = models.DateField()
    date_fin = models.DateField()
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='formations/', blank=True, null=True)
    publie = models.BooleanField(default=False)
    duree = models.CharField(max_length=50, blank=True, null=True)
               
    lieu = models.CharField(max_length=200, blank=True, null=True)    # 👈 ajouté
    capacite = models.IntegerField(default=0)         
    # Trimestre défini par l’admin
    trimestre = models.CharField(
        max_length=10,
        choices=[
            ('1er', '1er trimestre : septembre - novembre'),
            ('2eme', '2ème trimestre : décembre - février'),
            ('3eme', '3ème trimestre : mars - mai'),
            ('4eme', '4ème trimestre : juin - août'),
            ('mixte', 'Tous les trimestres'),
        ],
        default='mixte'
    )

    # Mode défini par l’admin
    mode = models.CharField(
        max_length=15,
        choices=[
            ('presentiel', 'Présentiel'),
            ('en_ligne', 'En ligne'),
            ('mixte', 'Présentiel et En ligne'),
        ],
        default='mixte'
    )
    
    lieu = models.CharField(max_length=255, blank=True, null=True) 
    horaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.titre} - {self.objet if self.objet else ''}"

# models.py

MODE_CHOICES = [
    ('présentiel', 'Présentiel'),
    ('en_ligne', 'En ligne'),
]

TRIMESTRE_CHOICES = [
    ('1er', '1er trimestre : septembre - novembre'),
            ('2eme', '2ème trimestre : décembre - février'),
            ('3eme', '3ème trimestre : mars - mai'),
            ('4eme', '4ème trimestre : juin - août'),
            
]


class Inscription(models.Model):
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name="inscriptions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=50, blank=True, null=True)

    email = models.EmailField()
    telephone = models.CharField(max_length=20, blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    mode = models.CharField(max_length=50, choices=MODE_CHOICES,)
    trimestre = models.CharField(max_length=10, choices=TRIMESTRE_CHOICES)


    statut = models.CharField(
        max_length=20,
        choices=[("en_attente", "En attente"), ("valide", "Validée"), ("refuse", "Refusée")],
        default="en_attente"
    )
    statut = models.CharField(
        max_length=20,
        choices=[('attente','En attente'), ('valide','Validée'), ('refuse','Refusée')],
        default='attente'
    )
    mode_paiement = models.CharField(
        max_length=50,
        choices=[
            ('carte','Carte bancaire'),
            ('paypal','PayPal'),
            ('especes','Espèces'),
            ('virement','Virement bancaire'),
        ],
        blank=True, null=True
    )
    
    mode_paiement = models.CharField(max_length=100, blank=True, null=True)
    paiement_info = models.TextField(blank=True, null=True)  # ou TextField si SQLite
    paiement_effectue = models.BooleanField(default=False)
    statut = models.CharField(max_length=50, default="En attente") 
    def __str__(self):
        return f"{self.nom} - {self.formation.titre}"

class Paiement(models.Model):
    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE)
    prenom = models.CharField(max_length=100, blank=False, null=False) 
    nom = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    mode_paiement = models.CharField(max_length=50)
    service = models.CharField(max_length=50, blank=True, null=True)
    details = models.JSONField(blank=True, null=True)  # stocke toutes les infos spécifiques
    statut = models.CharField(max_length=50, default="en attente")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Paiement {self.prenom} {self.nom} - {self.mode_paiement} ({self.statut})"


# ---------------------------------------------
# Réservations (lié au client)
# ---------------------------------------------
class ReservationClient(models.Model):  # <- nom unique pour éviter les doublons
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    objet = models.CharField(max_length=200)
    date = models.DateTimeField()
    statut = models.CharField(
        max_length=20,
        choices=[('En attente','En attente'), ('Acceptée','Acceptée'), ('Rejetée','Rejetée')],
        default='En attente'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.objet} - {self.client.username}"



class Profile(models.Model):
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Profil principal"
    



class Reponse(models.Model):
    message = models.ForeignKey(MessageContact, on_delete=models.CASCADE, related_name="reponses")
    contenu = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Réponse à {self.message.nom}"