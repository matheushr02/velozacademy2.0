import os
import django
import sys
from django.utils.text import slugify

# Configura o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'velozacademy.settings')
django.setup()

from cursos.models import Trilha, Curso

def criar_trilhas():
    # Lista de todas as trilhas a serem criadas
    trilhas_data = [
        {
            'nome': 'Aplicações IA com Python',
            'descricao': 'Aprenda a desenvolver aplicações práticas utilizando inteligência artificial e Python.',
            'slug': 'aplicacoes-ia',
            'area': 'ia',
            'total_cursos': 7,
            'total_horas': 42
        },
        {
            'nome': 'Dashboards Interativos com Python',
            'descricao': 'Crie visualizações de dados impressionantes e painéis interativos com Python.',
            'slug': 'dashboards',
            'area': 'dados',
            'total_cursos': 5,
            'total_horas': 35
        },
        {
            'nome': 'Python Office',
            'descricao': 'Automatize tarefas de escritório e aumente sua produtividade com Python.',
            'slug': 'python-office',
            'area': 'automacao',
            'total_cursos': 4,
            'total_horas': 28
        },
        {
            'nome': 'Visão Computacional',
            'descricao': 'Desenvolva sistemas que podem ver e interpretar o mundo visual.',
            'slug': 'visao-computacional',
            'area': 'ia',
            'total_cursos': 6,
            'total_horas': 38
        },
        {
            'nome': 'Data Science e Machine Learning',
            'descricao': 'Do básico ao avançado em ciência de dados e aprendizado de máquina.',
            'slug': 'data-science',
            'area': 'dados',
            'total_cursos': 8,
            'total_horas': 45
        },
        {
            'nome': 'Análise e Visualização de Dados',
            'descricao': 'Aprenda a extrair insights valiosos de conjuntos de dados e apresentá-los visualmente.',
            'slug': 'analise-dados',
            'area': 'dados',
            'total_cursos': 6,
            'total_horas': 32
        },
        {
            'nome': 'Trading Quantitativo',
            'descricao': 'Desenvolva estratégias de trading algorítmico e análise de mercado com Python.',
            'slug': 'trading',
            'area': 'dados',
            'total_cursos': 5,
            'total_horas': 30
        },
        {
            'nome': 'Desenvolvimento Web Fullstack',
            'descricao': 'Do front-end ao back-end, aprenda a construir aplicações web completas e modernas.',
            'slug': 'desenvolvimento-web',
            'area': 'dev',
            'total_cursos': 9,
            'total_horas': 48
        }
    ]
    
    # Verificar se existem trilhas no banco de dados
    if Trilha.objects.exists():
        print("Já existem trilhas no banco de dados. Deseja excluí-las e criar novas? (s/n)")
        resposta = input().lower()
        if resposta != 's':
            print("Operação cancelada.")
            return
        Trilha.objects.all().delete()
        print("Trilhas existentes excluídas.")
    
    # Criar as trilhas
    trilhas_criadas = []
    for trilha_data in trilhas_data:
        trilha = Trilha.objects.create(
            nome=trilha_data['nome'],
            slug=trilha_data['slug'],
            descricao=trilha_data['descricao'],
            area=trilha_data['area'],
            total_cursos=trilha_data['total_cursos'],
            total_horas=trilha_data['total_horas']
        )
        
        # Tentar associar cursos por palavras-chave correspondentes
        cursos_associados = []
        if trilha.slug == 'aplicacoes-ia':
            cursos_associados = Curso.objects.filter(titulo__icontains='IA') | Curso.objects.filter(descricao__icontains='Python')
        elif trilha.slug == 'dashboards':
            cursos_associados = Curso.objects.filter(titulo__icontains='dashboard') | Curso.objects.filter(descricao__icontains='dados')
        elif trilha.slug == 'python-office':
            cursos_associados = Curso.objects.filter(titulo__icontains='Python') | Curso.objects.filter(descricao__icontains='automação')
        elif trilha.slug == 'visao-computacional':
            cursos_associados = Curso.objects.filter(titulo__icontains='Python') | Curso.objects.filter(descricao__icontains='imagem')
        elif trilha.slug == 'data-science':
            cursos_associados = Curso.objects.filter(titulo__icontains='Python') | Curso.objects.filter(descricao__icontains='dados')
        else:
            # Para as outras trilhas, apenas pegar alguns cursos genericamente
            cursos_associados = Curso.objects.all()[:3]
        
        for curso in cursos_associados:
            trilha.cursos.add(curso)
        
        trilhas_criadas.append(trilha)
        print(f"Trilha '{trilha.nome}' criada com {trilha.cursos.count()} cursos associados.")
    
    print(f"Criadas {len(trilhas_criadas)} trilhas no banco de dados.")
    
    # Criar diretório para imagens de trilhas se não existir
    imagens_dir = os.path.join('static', 'images', 'trilhas')
    if not os.path.exists(imagens_dir):
        os.makedirs(imagens_dir)
        print(f"Diretório para imagens de trilhas criado em: {imagens_dir}")
    
    print("\nIMPORTANTE: Você precisará adicionar imagens para as trilhas em:")
    print(f"{os.path.abspath(imagens_dir)}")
    print("Nome dos arquivos esperados: ia.jpg, dashboards.jpg, office.jpg, visao.jpg, data-science.jpg, analise-dados.jpg, trading.jpg, web.jpg")

if __name__ == "__main__":
    print("Populando banco de dados com trilhas...")
    criar_trilhas()
    print("Processo concluído!") 