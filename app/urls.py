from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.signup, name='signup'),
    path('sign-in/', views.signin, name='signin'),
    path('sign-out/', views.signout, name='signout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]