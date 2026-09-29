from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import Temoin, MessageContact, Article ,Reservation,ArticleImage,Formation, Inscription


@admin.register(Temoin)
class TemoinAdmin(admin.ModelAdmin):
    list_display = ('nom', 'statut', 'date')
    list_filter = ('statut', 'date')
    search_fields = ('nom', 'commentaire')
    actions = ['accepter_temoins', 'refuser_temoins']

    def accepter_temoins(self, request, queryset):
        queryset.update(statut='accepte')
    accepter_temoins.short_description = "Accepter les témoignages sélectionnés"

    def refuser_temoins(self, request, queryset):
        queryset.update(statut='refuse')
    refuser_temoins.short_description = "Refuser les témoignages sélectionnés"


    
@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'sujet', 'date_envoi', 'statut')  # adapte selon ton modèle
    list_filter = ('statut', 'date_envoi')
    search_fields = ('nom', 'email', 'sujet')

class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1  # تقدري تزيدي العدد اللي بغيتي
   
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'categorie', 'date_pub', 'vues')
    search_fields = ('titre', 'contenu', 'auteur')
    list_filter = ('date_pub', 'categorie')
    
    inlines = [ArticleImageInline]

    


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("nom", "email", "date", "objet", "status", "created_at")
    list_filter = ("status", "date")
    search_fields = ("nom", "email", "objet")



class ReservationAdmin(admin.ModelAdmin):
    list_display = ("nom", "email", "date", "objet", "status", "created_at")
    list_filter = ("status", "date")
    search_fields = ("nom", "email", "objet")

    def save_model(self, request, obj, form, change):
        # Vérifie si on est en modification et si le statut change
        if change:
            old_obj = Reservation.objects.get(pk=obj.pk)
            super().save_model(request, obj, form, change)
            if old_obj.status != obj.status:  # Le statut a changé
                if obj.status == "accepted":
                    send_mail(
                        "Votre réservation est acceptée",
                        f"Bonjour {obj.nom},\n\nVotre réservation pour le {obj.date} a été acceptée ✅.",
                        settings.DEFAULT_FROM_EMAIL,
                        [obj.email],
                        fail_silently=False
                    )
                elif obj.status == "rejected":
                    send_mail(
                        "Votre réservation est refusée",
                        f"Bonjour {obj.nom},\n\nDésolé, votre réservation pour le {obj.date} a été refusée ❌.",
                        settings.DEFAULT_FROM_EMAIL,
                        [obj.email],
                        fail_silently=False
                    )
        else:
            # Si création, on peut juste sauvegarder
            super().save_model(request, obj, form, change)



@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ("titre", "objet", "date_debut", "date_fin", "duree", "lieu", "capacite", "prix", "publie")
    list_filter = ("publie",)
    search_fields = ("titre", "objet")

class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('nom', 'formation', 'mode', 'trimestre', 'statut', 'date_inscription')
    list_filter = ('mode', 'trimestre', 'statut' )
    search_fields = ('nom', 'email', 'telephone', 'formation__titre')

admin.site.register(Inscription, InscriptionAdmin)