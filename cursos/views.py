from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from users.models import Inscricao
from .models import Curso, Trilha, Modulo, Aula, ArquivoAula
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CursoForm, AulaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import Http404
import logging

#// remover/comentar logger quando em produção

logger = logging.getLogger(__name__)

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
        cursos = cursos.order_by('-data_criacao')
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
    modulos = curso.modulos.all().order_by('ordem')
    
    # Valores padrão
    inscrito = False
    progresso = 0
    first_aula_ordem = None
    
    for modulo in modulos:
        primeira_aula_do_modulo = modulo.aulas.all().order_by('ordem').first()
        if primeira_aula_do_modulo:
            first_aula_ordem = primeira_aula_do_modulo.ordem
            break

    # Here you would check if the user is enrolled and calculate progress
    # For now we just set defaults
    
    if request.user.is_authenticated:
        try:
            inscricao = Inscricao.objects.get(user=request.user, curso=curso)
            inscrito = True
            progresso = inscricao.progresso
        except Inscricao.DoesNotExist:
            pass
    
    context = {
        'curso': curso,
        'modulos': modulos,
        'inscrito': inscrito,
        'progresso': progresso,
        'first_aula_ordem': first_aula_ordem
    }
    
    return render(request, 'cursos/detalhe.html', context)

def trilha_cursos(request, trilha_slug):
    # Buscar a trilha pelo slug
    trilha = get_object_or_404(Trilha, slug=trilha_slug)
    
    # Obter os cursos associados à trilha
    cursos_da_trilha = trilha.cursos.all()
    
    context = {
        'trilha': trilha,
        'cursos': cursos_da_trilha,
    }
    
    return render(request, 'cursos/trilha.html', context)

def lista_trilhas(request):
    # Obter parâmetros de filtro
    search = request.GET.get('search', '')
    area_selecionada = request.GET.get('area', '')
    
    # Iniciar queryset
    trilhas = Trilha.objects.filter(publicada=True)
    
    # Aplicar filtros
    if search:
        trilhas = trilhas.filter(
            Q(titulo__icontains=search) | 
            Q(descricao__icontains=search)
        )
    
    if area_selecionada:
        trilhas = trilhas.filter(area=area_selecionada)
    
    context = {
        'trilhas': trilhas,
        'search': search,
        'area_selecionada': area_selecionada,
        #todo: tornar dinamico as opções da trilhas futuramente
    }
    return render(request, 'cursos/lista_trilhas.html', context)

#+ adicionar_curso refeito
def adicionar_curso(request):
    if not request.user.is_authenticated or not request.user.perfil.is_admin():
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect('cursos:lista')

    AulaFormSet = formset_factory(AulaForm, extra=1, can_delete=True)
    
    current_logger = logging.getLogger(__name__)
    
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        aula_formset = AulaFormSet(request.POST, request.FILES, prefix='aulas')
        
        current_logger = logging.getLogger(__name__)
        current_logger.debug("POST data: %s", request.POST)
        current_logger.debug("FILES data: %s", request.FILES)

        if form.is_valid() and aula_formset.is_valid():
            current_logger.debug("Form data is valid, trying to save...")
            #! continuar aqui debugando
            try:
                current_logger.debug("Form cleaned data: %s", form.cleaned_data)
                current_logger.debug("FormSet cleaned data: %s", [f.cleaned_data for f in aula_formset])
                # Salva o curso
                curso = form.save()
                print(f"Curso saved with ID {curso.id} and slug {curso.slug}")

                # Cria módulos padrão de aulas
                modulo = Modulo.objects.create(curso=curso, titulo="Módulo 1", ordem=1)
                
                current_logger.debug(f"Module created with ID {modulo.id}")

                #? Automaticamente verifica o tipo de conteudo dentro da aula do curso
                has_video = False
                has_text = False
                has_files = False
                
                #? Salva as aulas
                for i, aula_form in enumerate(aula_formset):
                    if aula_form.cleaned_data and not aula_form.cleaned_data.get('DELETE', False):
                        aula = Aula(
                            modulo=modulo, 
                            titulo=aula_form.cleaned_data['titulo'],
                            conteudo=aula_form.cleaned_data.get('conteudo', ''), 
                            duracao_minutos=aula_form.cleaned_data.get('duracao_minutos', 0),
                            video_embed_code=aula_form.cleaned_data.get('video_embed_code', ''),
                            ordem=i+1
                        )
                    
                        #? Verifica se o campo de video(file) foi preenchido     
                        video_key = f'aulas-{i}-video_file'
                        if video_key in request.FILES:
                            aula.video_file = request.FILES[video_key]
                        
                        if aula.video_file or (aula.video_embed_code and aula.video_embed_code.strip()):
                            has_video = True
                        if aula.conteudo and aula.conteudo.strip():
                            has_text = True
                        
                        aula.save()
                        
                        # Processamento de arquivos
                        arquivos_field_name = f'aulas-{i}-arquivos'
                        if arquivos_field_name in request.FILES:
                            uploaded_files_for_aula = request.FILES.getlist(arquivos_field_name)
                            if uploaded_files_for_aula:
                                has_files = True
                                for uploaded_file in uploaded_files_for_aula:
                                    ArquivoAula.objects.create(aula=aula,arquivo=uploaded_file, nome=uploaded_file.name)

                if has_video and has_text and has_files:
                    curso.tipo_conteudo = 'completo'
                elif has_video and has_text:
                    curso.tipo_conteudo = 'texto_video'
                elif has_video and has_files:
                    curso.tipo_conteudo = 'video_anexos'
                elif has_text and has_files:
                    curso.tipo_conteudo = 'texto_anexos'
                elif has_video:
                    curso.tipo_conteudo = 'video'
                elif has_text:
                    curso.tipo_conteudo = 'texto'
                elif has_files:
                    curso.tipo_conteudo = 'anexos'
                else:
                    curso.tipo_conteudo = 'nenhum'
                    
                #? Salva o curso com o tipo de conteúdo atualizado
                curso.save()                        
                
                messages.success(request, 'Curso adicionado com sucesso!')
                # Força uma resposta de redirecionamento imediata
                return redirect('cursos:detalhe', curso_slug=curso.slug)
                
            except Exception as e:
                # Se ocorrer qualquer erro, exclui o curso (rollback manual)
                if 'curso' in locals():
                    curso.delete()
                messages.error(request, f'Erro ao adicionar curso: {str(e)}')
                import traceback
                traceback.print_exc()
                return render(request, 'cursos/adicionar_curso.html', {'form': form, 'aula_formset': aula_formset})
                #return redirect('cursos:lista')
                
                
                #messages.success(request, 'Curso adicionado com sucesso!')
                #return redirect('cursos:detalhe', curso_slug=curso.slug)
        else:
            current_logger.debug("Form or Formset is invalid.")
            current_logger.debug("CursoForm errors: %s", form.errors.as_json() if form.errors else "No CursoForm errors")
            current_logger.debug("AulaFormSet errors: %s", aula_formset.errors if aula_formset.errors else "No AulaFormSet errors")
            current_logger.debug("AulaFormSet non_form_errors: %s", aula_formset.non_form_errors().as_json() if aula_formset.non_form_errors() else "No AulaFormSet non_form_errors")
            
            for field_name, error_list in form.errors.items():
                label = form.fields[field_name].label if field_name != '__all__' and field_name in form.fields else 'Geral do Curso'
                for error in error_list:
                    error_text = error.message if hasattr(error, 'message') else str(error)
                    messages.error(request, f"Erro em '{label}': {error_text}")
                
            if aula_formset.non_form_errors():
                for error in aula_formset.non_form_errors():
                    error_text = error.message if hasattr(error, 'message') else str(error)
                    messages.error(request, f"Erro no conjunto de aulas: {error_text}")

            for i, form_errors_dict in enumerate(aula_formset.errors):
                if form_errors_dict:
                    aula_form_instance = aula_formset.forms[i]

                    delete_field_name = aula_form_instance.add_prefix('DELETE')
                    if request.POST.get(delete_field_name):
                        #? Log que diz que marca aulas para deletar
                        current_logger.debug(f"Skipping errors for aula form {i} as it was marked for deletion.")
                        continue
                    
                    for field_name, error_list in form_errors_dict.items():
                        label = aula_form_instance.fields[field_name].label if field_name != '__all__' and field_name in aula_form_instance.fields else 'Geral da Aula'
                                                
                    

            has_aula_errors = any(f.errors for f in aula_formset.forms if not f.cleaned_data.get('DELETE'))
            if form.errors or has_aula_errors:
                messages.error(request, "Por favor, corrija os erros no formulário.")
            
            if 'imagem' in form.errors:
                messages.error(request, 'Ocorreu um erro com a imagem enviada. Por favor, verifique o formato e tamanho.')        

    else:
        form = CursoForm()
        aula_formset = AulaFormSet(prefix='aulas')
        
    return render(request, 'cursos/adicionar_curso.html', {'form': form, 'aula_formset': aula_formset})

def aula_view(request, curso_slug, aula_ordem):
    #? pega o curso por slug    
    curso = get_object_or_404(Curso, slug=curso_slug)
    
    logger.debug(f"Aula_view: Access attempt by user '{request.user.username if request.user.is_authenticated else 'Anonymous'}', for course: '{curso.slug}', aula_ordem: '{aula_ordem}'")
    
    can_access = False
    is_admin_user = False
    
    if request.user.is_authenticated:
        logger.debug(f"Aula_view: User '{request.user.username}' is authenticated.")
        if hasattr(request.user, 'perfil') and request.user.perfil.is_admin():
            can_access = True
            is_admin_user = True
            logger.debug(f"Aula_view: User '{request.user.username}' is admin. Access granted.")

        if not can_access:
            is_enrolled = Inscricao.objects.filter(user=request.user, curso=curso).exists()
            logger.debug(f"Aula_view: User '{request.user.username}' is enrolled in course '{curso.slug}'? {is_enrolled}")
            if is_enrolled:
                can_access = True
                logger.debug(f"Aula_view: User '{request.user.username}' is enrolled. Access granted.")
            else:
                course_is_free = hasattr(curso, 'is_free') and curso.is_free
                logger.debug(f"Aula_view: Course '{curso.slug}' is free? {course_is_free}")
                if course_is_free:
                    can_access = True
                    logger.debug(f"Aula_view: Course '{curso.slug}' is free. Access granted for user '{request.user.username}'.")
    else:
        logger.debug(f"Aula_view: User is not authenticated for this request.")

    logger.info(f"Aula_view: Final access decision for user '{request.user.username if request.user.is_authenticated else 'Anonymous'}' to course '{curso.slug}', aula_ordem '{aula_ordem}': {'Granted' if can_access else 'Denied'}")
            
    if not can_access:
        if not request.user.is_authenticated:
            messages.warning(request, 'Faça login para poder acessar.')
            return redirect(f"{reverse('users:login')}?next={request.path}")
        else:
            messages.warning(request, 'Você precisa se inscrever neste curso para assistir às aulas. ')
            return redirect('cursos:detalhe', curso_slug=curso.slug)

    try:
        aula = None
        for m in curso.modulos.all().order_by("ordem"):
            aula_candidata = m.aulas.filter(ordem=aula_ordem).first()
            if aula_candidata:
                aula = aula_candidata
                break

        if not aula:
            raise Http404("Aula não encontrada neste curso com a ordem especificada.")

    except Exception as e:
        logger.error(f"Error fetching aula: {e}")
        raise Http404("Aula não encontrada ou erro ao carregar.")

    aula_anterior = Aula.objects.filter(modulo__curso=curso, ordem__lt=aula_ordem).order_by('-ordem').first()
    proxima_aula = Aula.objects.filter(modulo__curso=curso, ordem__gt=aula_ordem).order_by('ordem').first()
    
    progresso_aula = 0
    aula_esta_concluida = False
    
    context = {
        'curso': curso,
        'aula': aula,
        'aula_anterior': aula_anterior,
        'proxima_aula': proxima_aula,
        'progresso_aula': progresso_aula,
        'aula_concluida': aula_esta_concluida,
        'is_admin_user': is_admin_user
    }
    
    return render(request, 'cursos/aula.html', context)

@login_required
def inscrever_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    
    if Inscricao.objects.filter(user=request.user, curso=curso).exists():
        messages.info(request, f'Você já está inscrito no curso {curso.titulo}!')
    else:
        Inscricao.objects.create(
            user=request.user,
            curso=curso,
            status='ativo',
            progresso=0
        )
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
    