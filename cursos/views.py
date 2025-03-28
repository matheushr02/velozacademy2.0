from django.shortcuts import render, get_object_or_404, redirect
from .models import Curso, Trilha, Modulo, Aula, ArquivoAula
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CursoForm, AulaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import Http404

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

def detalhe_curso(request, curso_slug):
    curso = get_object_or_404(Curso, slug=curso_slug)
    
    modulos = curso.modulos.all()
    
    # Add context variables needed by the template
    inscrito = False
    progresso = 0
    
    # Here you would check if the user is enrolled and calculate progress
    # For now we just set defaults
    
    if request.user.is_authenticated:
        pass
    
    context = {
        'curso': curso,
        'inscrito': inscrito,
        'progresso': progresso
    }
    
    return render(request, 'cursos/detalhe.html', context)

def trilha_cursos(request, trilha_slug):
    # Buscar a trilha pelo slug
    trilha = get_object_or_404(Trilha, slug=trilha_slug)
    
    # Obter os cursos associados à trilha
    cursos = trilha.cursos.all()
    
    return render(request, 'cursos/trilha.html', {
        'trilha_nome': trilha.nome,
        'trilha_slug': trilha_slug,
        'cursos': cursos
    })

def lista_trilhas(request):
    # Obter parâmetros de filtro
    search = request.GET.get('search', '')
    area = request.GET.get('area', '')
    
    # Iniciar queryset
    trilhas = Trilha.objects.all()
    
    # Aplicar filtros
    if search:
        trilhas = trilhas.filter(
            Q(nome__icontains=search) | 
            Q(descricao__icontains=search)
        )
    
    if area:
        trilhas = trilhas.filter(area=area)
    
    return render(request, 'cursos/lista_trilhas.html', {
        'trilhas': trilhas,
        'search': search,
        'area_selecionada': area
    })

#+ adicionar_curso refeito
def adicionar_curso(request):
    AulaFormSet = formset_factory(AulaForm, extra=1)
    
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        aula_formset = AulaFormSet(request.POST, request.FILES, prefix='aulas')
        
        if form.is_valid() and aula_formset.is_valid():
            try:
                # Salva o curso
                curso = form.save()
                
                # Cria módulos padrão de aulas
                modulo = Modulo.objects.create(curso=curso, titulo="Módulo 1", ordem=1)
                
                #? Salva as aulas
                for i, aula_form in enumerate(aula_formset):
                    if aula_form.cleaned_data and not aula_form.cleaned_data.get('DELETE', False):
                        aula = Aula(
                            modulo=modulo, 
                            titulo=aula_form.cleaned_data['titulo'],
                            conteudo=aula_form.cleaned_data.get('conteudo', ''), 
                            duracao_minutos=aula_form.cleaned_data.get('duracao_minutos', 0),
                            video_url=aula_form.cleaned_data.get('video_url', ''),
                            ordem=i+1
                        )
                    
                        #? Verifica se o campo de video(file) foi preenchido     
                        video_key = f'aulas-{i}-video_file'
                        if video_key in request.FILES:
                            aula.video_file = request.FILES[video_key]
                    
                        aula.save()
                        
                        # Processamento de arquivos
                        files = []
                        
                        j = 0
                        while True:
                            file_key = f'aulas-{i}-arquivos-{j}'
                            if file_key in request.FILES:
                                files.append(request.FILES[file_key])
                                j += 1
                            else:
                                if j == 0 and f'aulas-{i}-arquivos' in request.FILES:
                                    files.append(request.FILES[f'aulas-{i}-arquivos'])
                                break
                        
                        # Salva os arquivos da aula
                        for arquivo in files:
                            ArquivoAula.objects.create(aula=aula, arquivo=arquivo, nome=arquivo.name)
                
                messages.success(request, 'Curso adicionado com sucesso!')
                # Força uma resposta de redirecionamento imediata
                response = redirect('cursos:detalhe', curso_slug=curso.slug)
                response['Location'] = response.url
                return response
                
            except Exception as e:
                # Se ocorrer qualquer erro, exclui o curso (rollback manual)
                if 'curso' in locals():
                    curso.delete()
                messages.error(request, f'Erro ao adicionar curso: {str(e)}')
                return redirect('cursos:lista')
        else:
            if 'imagem' in form.errors:
                messages.error(request, 'Ocorreu um erro com a imagem enviada. Por favor, verifique o formato e tamanho.')        

    else:
        form = CursoForm()
        aula_formset = AulaFormSet(prefix='aulas')
        
    return render(request, 'cursos/adicionar_curso.html', {'form': form, 'aula_formset': aula_formset})

def aula_view(request, curso_slug, aula_ordem):
    #? pega o curso por slug    
    curso = get_object_or_404(Curso, slug=curso_slug)
    try:
        modulo = Modulo.objects.filter(curso=curso, aulas__ordem=aula_ordem).first()
        if not modulo:
            raise Http404("Aula não encontrada")
        
        aula = Aula.objects.filter(modulo=modulo, ordem=aula_ordem).first()
        if not aula:
            raise Http404("Aula não encontrada")
    except:
        raise Http404("Aula não encontrada")
    
    aula_anterior = Aula.objects.filter(modulo__curso=curso, ordem__lt=aula_ordem).order_by('-ordem').first()
    proxima_aula = Aula.objects.filter(modulo__curso=curso, ordem__gt=aula_ordem).order_by('ordem').first()
    
    progresso = 0
    aula_concluida = False
    
    context = {
        'curso': curso,
        'aula': aula,
        'aula_anterior': aula_anterior,
        'proxima_aula': proxima_aula,
        'progresso': progresso,
        'aula_concluida': aula_concluida,
    }
    
    return render(request, 'cursos/aula.html', context)

@login_required
def inscrever_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    
    # Normally, you would handle enrollment logic here
    # For now, just simulate success and redirect back
    messages.success(request, f'Você foi inscrito com sucesso no curso {curso.titulo}!')
    return redirect('cursos:detalhe', curso_slug=curso.slug)

#TODO: Implementar no database estas informações em uma futura implementação
@login_required 
def marcar_aula_concluida(request, aula_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    aula = get_object_or_404(Aula, id=aula_id)
    curso = aula.modulo.curso
    
    messages.success(request, 'Aula marcada como concluída!')
    return redirect('cursos:aula', curso_slug=curso.slug, aula_ordem=aula.ordem)

@login_required
def comentar_aula(request, aula_id):
    if not request.user.is_authenticated:
        return redirect('users:login')
    
    aula = get_object_or_404(Aula, id=aula_id)
    curso = aula.modulo.curso
    
    if request.method == 'POST':
        comentario = request.POST.get('comentario', '')
        if comentario:
            #todo: Salvar o comentário no banco de dados
            messages.success(request, 'Comentário adicionado com sucesso!')
            
    return redirect('cursos:aula', curso_slug=curso.slug, aula_ordem=aula.ordem)

@login_required
def responder_comentario(request, comentario_id):
    return redirect('cursos:aula', curso_slug='example', aula_ordem=1)

@login_required
def responder_quiz(request, atividade_id):
    return redirect('cursos:aula', curso_slug='example', aula_ordem=1)

@login_required
def entregar_projeto(request, atividade_id):
    #placeholder para o projeto
    #TODO: Implementar a lógica para entrega do projeto
    return redirect('cursos:aula', curso_slug='example', aula_ordem=1)
    