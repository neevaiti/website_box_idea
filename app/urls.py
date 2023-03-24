from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.signup, name='signup'),
    path('sign-in/', views.signin, name='signin'),
    path('sign-out/', views.signout, name='signout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('idees/', views.ideas_list, name='liste_idees'),
    path('nouvelle-idee/', views.new_idea, name='nouvelle_idee'),
    path('idee/<int:pk>/like/', views.like_idea, name='like_idee'),
    path('idee/<int:pk>/dislike/', views.dislike_idea, name='dislike_idee'),
    path('idee/<int:pk>/commenter/', views.new_comment, name='new_comment'),
    #path('idees-populaires/', views.ListeIdeesPopulaires.as_view(), name='liste_idees_populaires'),
    #path('idees-utilisateur/', views.ListeIdeesUtilisateur.as_view(), name='liste_idees_utilisateur'),
]