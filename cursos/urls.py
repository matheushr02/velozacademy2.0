from django.urls import path
from .views import lista_cursos, detalhe_curso, trilha_cursos, lista_trilhas, adicionar_curso, inscrever_curso

app_name = 'cursos'

urlpatterns = [
    path('', lista_cursos, name='lista'),
    path('<int:curso_id>/', detalhe_curso, name='detalhe'),
    path('<int:curso_id>/inscrever/', inscrever_curso, name='inscrever'),
    path('trilha/<slug:trilha_slug>/', trilha_cursos, name='trilha'),
    path('trilhas/', lista_trilhas, name='lista_trilhas'),
    path('adicionar/', adicionar_curso, name='adicionar_curso'),
] 