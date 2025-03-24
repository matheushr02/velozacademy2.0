import os
import django
from random import randint, choice
from decimal import Decimal

# Configura o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'velozacademy.settings')
django.setup()

from cursos.models import Curso, Modulo, Aula
from projetos.models import Tecnologia, Projeto, Etapa
from django.utils.text import slugify

def criar_cursos():
    # Limpar dados existentes (opcional)
    Curso.objects.all().delete()
    
    # Lista de cursos para adicionar
    cursos_data = [
        {
            'titulo': 'Python para Iniciantes',
            'descricao': 'Aprenda Python do zero, sem conhecimento prévio em programação.',
            'nivel': 'iniciante',
            'preco': Decimal('99.90'),
            'desconto': Decimal('20.00'),
        },
        {
            'titulo': 'Django Web Development',
            'descricao': 'Desenvolvimento web completo com Django, do básico ao avançado.',
            'nivel': 'intermediario',
            'preco': Decimal('159.90'),
            'desconto': Decimal('30.00'),
        },
        {
            'titulo': 'React: Desenvolvimento Frontend',
            'descricao': 'Crie interfaces modernas e reativas com React e JavaScript.',
            'nivel': 'intermediario',
            'preco': Decimal('149.90'),
            'desconto': Decimal('0.00'),
        },
        {
            'titulo': 'JavaScript Avançado',
            'descricao': 'Conceitos avançados de JavaScript, incluindo promises, async/await, e padrões de design.',
            'nivel': 'avancado',
            'preco': Decimal('179.90'),
            'desconto': Decimal('30.00'),
        },
    ]
    
    cursos_criados = []
    
    for curso_data in cursos_data:
        curso = Curso.objects.create(
            titulo=curso_data['titulo'],
            slug=slugify(curso_data['titulo']),
            descricao=curso_data['descricao'],
            nivel=curso_data['nivel'],
            preco=curso_data['preco'],
            desconto=curso_data['desconto'],
        )
        cursos_criados.append(curso)
        
        # Adicionar módulos para cada curso
        for i in range(1, 5):  # 4 módulos por curso
            modulo = Modulo.objects.create(
                curso=curso,
                titulo=f"Módulo {i}: {choice(['Fundamentos', 'Conceitos Básicos', 'Teoria', 'Prática', 'Avançado'])}",
                descricao=f"Descrição detalhada do módulo {i} do curso {curso.titulo}",
                ordem=i
            )
            
            # Adicionar aulas para cada módulo
            for j in range(1, 6):  # 5 aulas por módulo
                Aula.objects.create(
                    modulo=modulo,
                    titulo=f"Aula {j}: {choice(['Introdução', 'Conceitos', 'Exemplos', 'Exercícios', 'Projeto'])}",
                    conteudo=f"Conteúdo detalhado da aula {j} do módulo {modulo.titulo}",
                    ordem=j,
                    duracao_minutos=randint(10, 60)
                )
    
    print(f"Criados {len(cursos_criados)} cursos com seus módulos e aulas")
    return cursos_criados

def criar_projetos():
    # Limpar dados existentes (opcional)
    Projeto.objects.all().delete()
    
    # Criar tecnologias
    tecnologias = []
    for tech in ['Python', 'Django', 'JavaScript', 'React', 'HTML', 'CSS', 'Node.js', 'Flask']:
        tecnologia, created = Tecnologia.objects.get_or_create(nome=tech)
        tecnologias.append(tecnologia)
    
    # Lista de projetos para adicionar
    projetos_data = [
        {
            'titulo': 'API RESTful com Django',
            'descricao': 'Desenvolvimento de uma API RESTful completa usando Django Rest Framework',
            'objetivo': 'Aprender a criar APIs modernas seguindo os princípios REST',
            'dificuldade': 'medio',
            'tempo_estimado_horas': 20,
            'tecnologias': ['Python', 'Django'],
        },
        {
            'titulo': 'Blog com React e Django',
            'descricao': 'Crie um blog completo com React no frontend e Django no backend',
            'objetivo': 'Integrar frontend React com uma API Django',
            'dificuldade': 'dificil',
            'tempo_estimado_horas': 40,
            'tecnologias': ['Python', 'Django', 'JavaScript', 'React'],
        },
        {
            'titulo': 'Portfólio Pessoal',
            'descricao': 'Desenvolva um site de portfólio para mostrar seus projetos',
            'objetivo': 'Criar um site responsivo e moderno para exibir trabalhos',
            'dificuldade': 'facil',
            'tempo_estimado_horas': 15,
            'tecnologias': ['HTML', 'CSS', 'JavaScript'],
        },
        {
            'titulo': 'E-commerce Simples',
            'descricao': 'Loja virtual básica com catálogo de produtos e carrinho de compras',
            'objetivo': 'Entender os fundamentos de um sistema de e-commerce',
            'dificuldade': 'medio',
            'tempo_estimado_horas': 30,
            'tecnologias': ['Python', 'Django', 'HTML', 'CSS', 'JavaScript'],
        },
    ]
    
    projetos_criados = []
    
    for projeto_data in projetos_data:
        projeto = Projeto.objects.create(
            titulo=projeto_data['titulo'],
            slug=slugify(projeto_data['titulo']),
            descricao=projeto_data['descricao'],
            objetivo=projeto_data['objetivo'],
            dificuldade=projeto_data['dificuldade'],
            tempo_estimado_horas=projeto_data['tempo_estimado_horas'],
        )
        
        # Adicionar tecnologias
        for tech_nome in projeto_data['tecnologias']:
            tech = Tecnologia.objects.get(nome=tech_nome)
            projeto.tecnologias.add(tech)
        
        projetos_criados.append(projeto)
        
        # Adicionar etapas para cada projeto
        for i in range(1, 6):  # 5 etapas por projeto
            Etapa.objects.create(
                projeto=projeto,
                titulo=f"Etapa {i}: {choice(['Planejamento', 'Setup', 'Desenvolvimento', 'Testes', 'Deploy'])}",
                descricao=f"Descrição da etapa {i} do projeto {projeto.titulo}",
                instrucoes=f"Instruções detalhadas para completar a etapa {i}:\n1. Primeiro passo\n2. Segundo passo\n3. Terceiro passo",
                ordem=i
            )
    
    print(f"Criados {len(projetos_criados)} projetos com suas etapas")
    return projetos_criados

if __name__ == "__main__":
    print("Populando banco de dados...")
    criar_cursos()
    criar_projetos()
    print("Banco de dados populado com sucesso!") 