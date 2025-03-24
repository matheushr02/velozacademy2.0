from django.urls import path
from .views import lista_cursos, detalhe_curso, trilha_cursos, lista_trilhas

app_name = 'cursos'

urlpatterns = [
    path('', lista_cursos, name='lista'),
    path('<int:curso_id>/', detalhe_curso, name='detalhe'),
    path('trilha/<slug:trilha_slug>/', trilha_cursos, name='trilha'),
    path('trilhas/', lista_trilhas, name='lista_trilhas'),
] 