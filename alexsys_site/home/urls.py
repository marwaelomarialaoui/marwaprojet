from django.urls import path


from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views  # <-- important

urlpatterns = [
    path('', views.index, name='index'),
    path('nos-solutions/', views.nos_solutions, name='nos_solutions'),
    path('dashboard/', views.dashboard, name='dashboard'),  # dashboard
     path('a-propos/', views.a_propos, name='a_propos'),
# Messages / Témoignages
 
    path('contact/', views.contact, name='contact'),
    path('temoins/', views.temoins, name='temoins'),
    
   
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    
    path('messages-contact/', views.messages_contact, name='messages_contact'),
   
    path('changer-statut/<int:id>/<str:new_statut>/', views.changer_statut_message, name='changer_statut'),
    path('changer-statut-temoin/<int:temoin_id>/<str:nouveau_statut>/', views.changer_statut_temoin, name='changer_statut_temoin'),
    path('messages/accepter/<int:id>/', views.accepter_message, name='accepter_message'),
    path('messages/refuser/<int:id>/', views.refuser_message, name='refuser_message'),
    path('messages/repondre/<int:id>/', views.envoyer_reponse, name='envoyer_reponse'),

    path('mes-messages/', views.mes_messages, name='mes_messages'),
   
    path('ajouter-temoin/', views.ajouter_temoin, name='ajouter_temoin'),
    path('gerer_temoins/', views.gerer_temoins, name='gerer_temoins'),  # Admin direct
    path('accepter_temoin/<int:temoin_id>/', views.accepter_temoin, name='accepter_temoin'),
    path('refuser_temoin/<int:temoin_id>/', views.refuser_temoin, name='refuser_temoin'),
    

       # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:article_id>/', views.blog_detail, name='blog_detail'),
    


    path('admin-panel/blog/', views.gerer_blog, name='gerer_blog'),
    path('admin-panel/blog/ajouter/', views.ajouter_article, name='ajouter_article'),
    
    path('article/modifier/<int:id>/', views.modifier_article, name='modifier_article'),
    path('article/supprimer/<int:id>/', views.supprimer_article, name='supprimer_article'),
    
    # Réservations côté client
   

    path('mes-reservations/', views.reservations_client_list, name='reservations_client_list'),
    path('reservation/<int:pk>/client/', views.reservation_client_detail, name='reservation_client_detail'),
    path('reservation/', views.reserver, name='reserver'),  # URL pour le formulaire de réservation
    path('reservation/success/', views.reservation_success, name='reservation_success'),
    path('reservation/create/', views.create_reservation, name='create_reservation'),
    # Côté admin (panel custom)
    path('reservations/', views.reservations_list, name='reservations_list'),
    path('admin-panel/reservations/', views.gerer_reservations, name='gerer_reservations'),
    path('reservation/<int:pk>/<str:status>/', views.update_reservation_status, name='update_reservation_status'),
    path("admin/reservations/<int:pk>/accepter/", views.reservation_accept, name="reservation_accept"),
    path("admin/reservations/<int:pk>/refuser/", views.reservation_decline, name="reservation_decline"),
    path("admin/reservations/<int:pk>/modifier/", views.reservation_edit, name="reservation_edit"),


     # Formations
    path('admin-panel/formations/', views.gerer_formations, name='gerer_formations'),
    path('admin-panel/formations/ajouter/', views.ajouter_formation, name='ajouter_formation'),
    # urls.py (f app home)
    path('admin-panel/formations/modifier/<int:id>/', views.modifier_formation, name='modifier_formation'),
    path('admin-panel/formations/supprimer/<int:id>/', views.supprimer_formation, name='supprimer_formation'),
    path('formations/', views.liste_formations, name='liste_formations'),
    path('formations/<int:pk>/', views.detail_formation, name='detail_formation'),
    
    path('inscription/<int:formation_id>/', views.inscription_formation, name='inscription_formation'),
    path('admin-panel/inscriptions/', views.gerer_inscriptions, name='gerer_inscriptions'),
    path('admin-panel/inscriptions/<int:pk>/<str:status>/', views.update_inscription_status, name='update_inscription_status'),
    path('admin-panel/inscriptions/accepter/<int:insc_id>/', views.accepter_inscription, name='accepter_inscription'),
    path('admin-panel/inscriptions/refuser/<int:insc_id>/', views.refuser_inscription, name='refuser_inscription'),
    path('mes-inscriptions/', views.mes_inscriptions, name='mes_inscriptions'),
    path('choisir-paiement/<int:inscription_id>/', views.choisir_paiement, name='choisir_paiement'),
    path('gerer-paiements/', views.gerer_paiements, name='gerer_paiements'),
    path('valider-paiement/<int:inscription_id>/', views.valider_paiement, name='valider_paiement'),
    path('paiements/', views.gestion_paiements, name='paiements'),
    path('paiements/', views.gestion_paiements, name='paiements'),



    # Ajouter témoignage côté client
    path('ajouter-temoin/', views.ajouter_temoin, name='ajouter_temoin'),


    
   
    path('mes-reservations/', views.reservations_client_list, name='mes_reservations'),
    
   

   # admin code (page pour entrer le code secret)
    path('admin-panel/code/', views.admin_panel_code, name='admin_panel_code'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    

    # Profil client
    path('modifier-profil/', views.modifier_profil, name='modifier_profil'),

    # Réservations client
    path('reservation/nouvelle/', views.nouvelle_reservation, name='nouvelle_reservation'),
    path('reservation/<int:id>/', views.detail_reservation, name='detail_reservation'),
    path('reservation/<int:id>/annuler/', views.annuler_reservation, name='annuler_reservation'),

    # Messages client
    
    path('message/<int:id>/', views.detail_message, name='detail_message'),
   
    # connexion user
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
]

