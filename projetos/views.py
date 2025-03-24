from django.shortcuts import render, get_object_or_404
from .models import Projeto, Tecnologia
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def lista_projetos(request):
    # Obter parâmetros de filtro
    search = request.GET.get('search', '')
    categoria = request.GET.get('categoria', '')
    dificuldade = request.GET.get('dificuldade', '')
    
    # Iniciar queryset
    projetos = Projeto.objects.all()
    
    # Aplicar filtros de busca
    if search:
        projetos = projetos.filter(
            Q(titulo__icontains=search) | 
            Q(descricao__icontains=search) |
            Q(objetivo__icontains=search)
        )
    
    # Filtrar por dificuldade
    if dificuldade:
        projetos = projetos.filter(dificuldade=dificuldade)
    
    # Filtrar por tecnologia (como "categoria")
    if categoria and categoria != 'todos':
        # Tenta converter a categoria em um ID de tecnologia se for numérico
        try:
            categoria_id = int(categoria)
            projetos = projetos.filter(tecnologias__id=categoria_id)
        except ValueError:
            # Se não for um ID numérico, ignoramos o filtro
            pass
    
    # Paginação
    paginator = Paginator(projetos, 9)  # 9 projetos por página
    page = request.GET.get('page')
    try:
        projetos_paginados = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não for um inteiro, exibe a primeira página
        projetos_paginados = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo, exibe a última página
        projetos_paginados = paginator.page(paginator.num_pages)
    
    # Preparar dificuldades para o filtro dropdown
    dificuldades = Projeto.DIFICULDADE_CHOICES
    
    # Obter tecnologias para o filtro dropdown
    tecnologias = Tecnologia.objects.all()
    categorias = [(tech.id, tech.nome) for tech in tecnologias]
    
    context = {
        'projetos': projetos_paginados,
        'dificuldades': dificuldades,
        'categorias': categorias,
        'search': search,
        'dificuldade_selecionada': dificuldade,
        'categoria_selecionada': categoria,
        'total_projetos': projetos.count()
    }
    
    return render(request, 'projetos/lista.html', context)

def detalhe_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    return render(request, 'projetos/detalhe.html', {'projeto': projeto})
