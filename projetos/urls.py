from django.urls import path
from .views import lista_projetos, detalhe_projeto

app_name = 'projetos'

urlpatterns = [
    path('', lista_projetos, name='lista'),
    path('<int:projeto_id>/', detalhe_projeto, name='detalhe'),
] 