from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.users, name='users'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('image/', views.image, name='image'),
    path('text/', views.text, name='text'),
]