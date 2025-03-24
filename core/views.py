from django.shortcuts import render
from cursos.models import Curso
from projetos.models import Projeto

def home(request):
    cursos = Curso.objects.all()[:3]  # Get latest 3 courses
    projetos = Projeto.objects.all()[:3]  # Get latest 3 projects
    
    context = {
        'cursos': cursos,
        'projetos': projetos,
    }
    return render(request, 'core/home.html', context)
