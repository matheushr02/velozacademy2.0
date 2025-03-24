from django.shortcuts import render, get_object_or_404
from .models import Curso
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def lista_cursos(request):
    # Obter parâmetros de filtro
    search = request.GET.get('search', '')
    categoria = request.GET.get('categoria', '')
    nivel = request.GET.get('nivel', '')
    ordenar = request.GET.get('ordenar', 'recentes')
    
    # Iniciar queryset
    cursos = Curso.objects.all()
    
    # Aplicar filtros de busca
    if search:
        cursos = cursos.filter(
            Q(titulo__icontains=search) | 
            Q(descricao__icontains=search)
        )
    
    # Filtrar por nível
    if nivel:
        cursos = cursos.filter(nivel=nivel)
    
    # Ordenação
    if ordenar == 'recentes':
        cursos = cursos.order_by('-criado_em')
    elif ordenar == 'populares':
        # Aqui seria ideal ter um campo de popularidade, mas por simplicidade usamos id
        cursos = cursos.order_by('-id')
    elif ordenar == 'horas_asc':
        # Suponha que temos um método que calcula horas totais
        cursos = cursos.order_by('modulos__aulas__duracao_minutos')
    elif ordenar == 'horas_desc':
        cursos = cursos.order_by('-modulos__aulas__duracao_minutos')
    
    # Paginação
    paginator = Paginator(cursos, 9)  # 9 cursos por página
    page = request.GET.get('page')
    try:
        cursos_paginados = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não for um inteiro, exibe a primeira página
        cursos_paginados = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo, exibe a última página
        cursos_paginados = paginator.page(paginator.num_pages)
    
    # Preparar níveis para o filtro dropdown
    niveis = [
        ('iniciante', 'Iniciante'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
    ]
    
    # Aqui seriam as categorias reais do banco de dados
    categorias = [
        ('programacao', 'Programação'),
        ('data-science', 'Ciência de Dados'),
        ('ia', 'Inteligência Artificial'),
        ('automacao', 'Automação'),
        ('web', 'Desenvolvimento Web'),
    ]
    
    context = {
        'cursos': cursos_paginados,
        'niveis': niveis,
        'categorias': categorias,
        'search': search,
        'nivel_selecionado': nivel,
        'categoria_selecionada': categoria,
        'ordenar': ordenar,
    }
    
    return render(request, 'cursos/lista.html', context)

def detalhe_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    return render(request, 'cursos/detalhe.html', {'curso': curso})

def trilha_cursos(request, trilha_slug):
    trilhas = {
        'aplicacoes-ia': 'Aplicações IA com Python',
        'dashboards': 'Dashboards Interativos com Python',
        'python-office': 'Python Office',
        'visao-computacional': 'Visão Computacional',
        'data-science': 'Data Science e Machine Learning',
        'analise-dados': 'Análise e Visualização de Dados',
        'trading': 'Trading Quantitativo'
    }
    
    trilha_nome = trilhas.get(trilha_slug, 'Trilha não encontrada')
    
    # Filtrando cursos que pertencem à trilha (simulação)
    # Em um ambiente real, você teria um modelo de Trilha relacionado a Curso
    if trilha_slug == 'aplicacoes-ia':
        cursos = Curso.objects.filter(Q(titulo__icontains='IA') | Q(descricao__icontains='Inteligência Artificial'))
    elif trilha_slug == 'dashboards':
        cursos = Curso.objects.filter(Q(titulo__icontains='Dashboard') | Q(descricao__icontains='Dashboard'))
    elif trilha_slug == 'python-office':
        cursos = Curso.objects.filter(Q(titulo__icontains='Office') | Q(descricao__icontains='Automação'))
    elif trilha_slug == 'visao-computacional':
        cursos = Curso.objects.filter(Q(titulo__icontains='Visão') | Q(descricao__icontains='Imagem'))
    elif trilha_slug == 'data-science':
        cursos = Curso.objects.filter(Q(titulo__icontains='Data') | Q(descricao__icontains='Machine Learning'))
    elif trilha_slug == 'analise-dados':
        cursos = Curso.objects.filter(Q(titulo__icontains='Análise') | Q(descricao__icontains='Dados'))
    elif trilha_slug == 'trading':
        cursos = Curso.objects.filter(Q(titulo__icontains='Trading') | Q(descricao__icontains='Financeiro'))
    else:
        cursos = Curso.objects.all()
    
    return render(request, 'cursos/trilha.html', {
        'trilha_nome': trilha_nome,
        'trilha_slug': trilha_slug,
        'cursos': cursos
    })

def lista_trilhas(request):
    # Lista de todas as trilhas disponíveis
    trilhas = [
        {
            'slug': 'aplicacoes-ia',
            'nome': 'Aplicações IA com Python',
            'descricao': 'Aprenda a desenvolver aplicações práticas utilizando inteligência artificial e Python.',
            'imagem': '/static/images/trilhas/ia.jpg'
        },
        {
            'slug': 'dashboards',
            'nome': 'Dashboards Interativos com Python',
            'descricao': 'Crie visualizações de dados impressionantes e painéis interativos com Python.',
            'imagem': '/static/images/trilhas/dashboards.jpg'
        },
        {
            'slug': 'python-office',
            'nome': 'Python Office',
            'descricao': 'Automatize tarefas de escritório e aumente sua produtividade com Python.',
            'imagem': '/static/images/trilhas/office.jpg'
        },
        {
            'slug': 'visao-computacional',
            'nome': 'Visão Computacional',
            'descricao': 'Desenvolva sistemas que podem ver e interpretar o mundo visual.',
            'imagem': '/static/images/trilhas/visao.jpg'
        },
        {
            'slug': 'data-science',
            'nome': 'Data Science e Machine Learning',
            'descricao': 'Aprenda a extrair conhecimento e insights de dados usando algoritmos avançados.',
            'imagem': '/static/images/trilhas/datascience.jpg'
        },
        {
            'slug': 'analise-dados',
            'nome': 'Análise e Visualização de Dados',
            'descricao': 'Transforme dados brutos em informações úteis através de visualizações poderosas.',
            'imagem': '/static/images/trilhas/dados.jpg'
        },
        {
            'slug': 'trading',
            'nome': 'Trading Quantitativo',
            'descricao': 'Crie estratégias de investimento automatizadas baseadas em dados e algoritmos.',
            'imagem': '/static/images/trilhas/trading.jpg'
        },
    ]
    
    return render(request, 'cursos/lista_trilhas.html', {'trilhas': trilhas})
