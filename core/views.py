from django.shortcuts import render
from cursos.models import Curso
from projetos.models import Projeto
import random

def home(request):
    # Obter todos os cursos e projetos
    todos_cursos = list(Curso.objects.all())
    todos_projetos = list(Projeto.objects.all())
    
    # Selecionar 3 cursos aleatórios para exibir como "cursos em destaque" na página inicial
    # Se houver menos de 3 cursos, usa todos os disponíveis
    cursos_destaque = random.sample(todos_cursos, min(3, len(todos_cursos)))
    
    # Selecionar 3 projetos aleatórios para exibir como "projetos populares" na página inicial
    # Se houver menos de 3 projetos, usa todos os disponíveis
    projetos_populares = random.sample(todos_projetos, min(3, len(todos_projetos)))
    
    context = {
        'cursos_destaque': cursos_destaque,
        'projetos_populares': projetos_populares,
    }
    return render(request, 'core/home.html', context)
