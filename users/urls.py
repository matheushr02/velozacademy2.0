from django.urls import path
from .views import login_view, logout_view, registro_view, perfil_view, recuperar_senha_view

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registro/', registro_view, name='registro'),
    path('perfil/', perfil_view, name='perfil'),
    path('recuperar-senha/', recuperar_senha_view, name='recuperar_senha'),
] 