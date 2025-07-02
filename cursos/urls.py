from django.urls import path
from .views import lista_cursos, detalhe_curso, trilha_cursos, lista_trilhas, adicionar_curso, inscrever_curso, aula_view, marcar_aula_concluida, comentar_aula, responder_comentario, responder_quiz, entregar_projeto
from cursos import views

app_name = 'cursos'
#! IMPORTANTE: no django ordem importa na urls, caminhos especifocos devem vir antes de caminhos genericos; Fazer errado vai fazer com que o django não encontre a url correta e mostrar a tela de debug ou 404;
urlpatterns = [
    path('', lista_cursos, name='lista'),
    path('trilhas/', lista_trilhas, name='lista_trilhas'),
    path('trilha/<slug:trilha_slug>/', trilha_cursos, name='detalhe_trilha'),
    path('adicionar/', adicionar_curso, name='adicionar_curso'),
    path('aula/<int:aula_id>/marcar-concluida/', marcar_aula_concluida, name='marcar_concluida'),
    path('aula/<int:aula_id>/comentar/', comentar_aula, name='comentar_aula'),
    path('comentario/<int:comentario_id>/responder/', responder_comentario, name='responder_comentario'),
    path('atividade/<int:atividade_id>/responder-quiz/', responder_quiz, name='responder_quiz'),
    path('atividade/<int:atividade_id>/entregar-projeto/', entregar_projeto, name='entregar_projeto'),
    path('<slug:curso_slug>/aula/<int:aula_id>/', views.aula_view, name='aula'),
    path('<slug:curso_slug>/', detalhe_curso, name='detalhe'),
    path('<int:curso_id>/inscrever/', inscrever_curso, name='inscrever'),
] 