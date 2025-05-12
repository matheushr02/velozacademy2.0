from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from cursos.models import Curso, Trilha, Modulo, Aula
from users.models import Inscricao, Perfil
from django.db.models import Count, Sum

def is_admin(user):
    """Verifica se o usuário é um administrador."""
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def dashboard_home(request):
    """View para a página principal da dashboard administrativa."""
    # Contagem de todos os dados importantes
    stats = {
        'total_usuarios': User.objects.count(),
        'total_cursos': Curso.objects.count(),
        'total_trilhas': Trilha.objects.count(),
        'total_modulos': Modulo.objects.count(),
        'total_aulas': Aula.objects.count(),
        'total_inscricoes': Inscricao.objects.count(),
    }
    
    # Níveis dos cursos
    niveis_cursos = list(Curso.objects.values('nivel').annotate(count=Count('id')))
    total_cursos = stats['total_cursos'] or 1  # Evitar divisão por zero
    for nivel in niveis_cursos:
        nivel['porcentagem'] = int((nivel['count'] / total_cursos) * 100)
    
    # Áreas das trilhas
    areas_trilhas = list(Trilha.objects.values('area').annotate(count=Count('id')))
    total_trilhas = stats['total_trilhas'] or 1  # Evitar divisão por zero
    for area in areas_trilhas:
        area['porcentagem'] = int((area['count'] / total_trilhas) * 100)
    
    # Últimos 5 usuários cadastrados
    ultimos_usuarios = User.objects.order_by('-date_joined')[:5]
    
    # Últimos 5 cursos cadastrados
    ultimos_cursos = Curso.objects.order_by('-criado_em')[:5]
    
    context = {
        'stats': stats,
        'niveis_cursos': niveis_cursos,
        'areas_trilhas': areas_trilhas,
        'ultimos_usuarios': ultimos_usuarios,
        'ultimos_cursos': ultimos_cursos,
    }
    
    return render(request, 'dashboard/home.html', context)
