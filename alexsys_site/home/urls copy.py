from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('temoins/', views.temoins, name='temoins'),
    path('dashboard/', views.dashboard, name='dashboard'),  # dashboard
    path('a-propos/', views.a_propos, name='a_propos'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('gerer-temoins/', views.gerer_temoins, name='gerer_temoins'),
    path('messages-contact/', views.messages_contact, name='messages_contact'),
    path('gerer-formations/', views.gerer_formations, name='gerer_formations'),
    path('changer-statut/<int:id>/<str:new_statut>/', views.changer_statut_message, name='changer_statut'),
    path('message/<int:id>/supprimer/', views.supprimer_message, name='supprimer_message'),
    path('message/<int:id>/', views.voir_message, name='voir_message'),  # ➕ AJOUTE ÇA si tu veux voir un message seul
    path('nos-solutions/', views.nos_solutions, name='nos_solutions'),
  

]
