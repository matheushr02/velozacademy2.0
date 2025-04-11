# VelozAcademy - Plataforma de Ensino de Programação

A VelozAcademy é uma plataforma de ensino de programação focada em projetos práticos e aprendizado baseado em problemas do mundo real.

## Funcionalidades

- **Cursos**: Organização de cursos por módulos e aulas, com conteúdo em diversos formatos (vídeo, texto, códigos, etc)
- **Projetos**: Projetos práticos organizados por níveis de dificuldade para aplicação do conhecimento
- **Trilhas de aprendizado**: Caminhos recomendados para aprender uma tecnologia ou área específica
- **Sistema de usuários**: Cadastro, autenticação, perfil, e progresso do estudante
- **Fórum de dúvidas**: Comunicação e troca de conhecimento entre alunos e instrutores

## Tecnologias utilizadas

- **Backend**: Django 4.2
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Banco de dados**: SQLite (desenvolvimento)
- **Ferramentas**: Git, Docker (opcional)

## Instalação e Configuração

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/velozacademy.git
```
no terminal mude para a pasta do projeto
```bash
cd velozacademy2.0
```

2. Crie um ambiente virtual
```bash
python -m venv venv
```
2.1 Ative seu ambiente virtual
```bash
venv\Scripts\activate #CASO FOR WINDOWS
```

```bash
source venv/bin/activate #CASO FOR LINUX
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute as migrações do banco de dados:
```bash
python manage.py migrate
```

5. Crie um superusuário (admin) (**PULE ESTA ETAPA**):
```bash
python manage.py createsuperuser
```

6. Popule o banco de dados com dados iniciais:
```bash
# Criar cursos e projetos
python populate_db.py
```
```bash
# Criar trilhas de aprendizado
python populate_trilhas.py
```

7. Adicione imagens para as trilhas:
   - Crie ou obtenha imagens para representar cada trilha
   - Coloque-as na pasta `static/images/trilhas/` com os seguintes nomes:
     - ia.jpg
     - dashboards.jpg
     - office.jpg
     - visao.jpg
     - data-science.jpg
     - analise-dados.jpg
     - trading.jpg
     - web.jpg

8. Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

Acesse o site em http://127.0.0.1:8000/ e o painel administrativo em http://127.0.0.1:8000/admin/

## Observações importantes

- **Banco de dados**: O arquivo do banco de dados (db.sqlite3) está no `.gitignore` e não é enviado para o GitHub. Isso significa que ao clonar o repositório, o banco estará vazio até que você execute os scripts de população (`populate_db.py` e `populate_trilhas.py`).

- **Arquivos de mídia**: Os diretórios `media/` e `static/images/trilhas/` que contêm imagens enviadas pelos usuários e imagens das trilhas também não são versionados. Certifique-se de adicionar as imagens necessárias após a clonagem.

- **Administração de conteúdo**: Após configurar o ambiente, você pode adicionar, editar ou remover cursos, projetos e trilhas através do painel de administração (http://127.0.0.1:8000/admin/).

## Estrutura do projeto

- `core/`: App principal com views compartilhadas
- `cursos/`: App para gerenciamento de cursos, materiais e trilhas
- `projetos/`: App para projetos práticos
- `users/`: App para gerenciamento de usuários e perfis
- `templates/`: Templates HTML
- `static/`: Arquivos estáticos (CSS, JS, imagens)
- `media/`: Uploads de usuários (avatares, certificados, etc)
- `populate_db.py`: Script para popular o banco com cursos e projetos
- `populate_trilhas.py`: Script para popular o banco com trilhas

## Desenvolvimento

Para contribuir com o projeto, siga estas etapas:

1. Crie uma branch para sua funcionalidade: `git checkout -b feature/nome-da-funcionalidade`
2. Faça suas alterações e commit: `git commit -m 'Adiciona nova funcionalidade'`
3. Envie para o repositório: `git push origin feature/nome-da-funcionalidade`
4. Crie um Pull Request

## Backup e Restauração

Para projetos em produção, é recomendável fazer backup regular do banco de dados:

```bash
# Backup
python manage.py dumpdata > backup.json

# Restauração
python manage.py loaddata backup.json
```

## Licença

Este projeto está licenciado sob a licença MIT.
