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

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/velozacademy.git
cd velozacademy
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute as migrações do banco de dados:
```bash
python manage.py migrate
```

5. Crie um superusuário (admin):
```bash
python manage.py createsuperuser
```

6. Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

Acesse o site em http://127.0.0.1:8000/ e o painel administrativo em http://127.0.0.1:8000/admin/

## Estrutura do projeto

- `core/`: App principal com views compartilhadas
- `cursos/`: App para gerenciamento de cursos e materiais
- `projetos/`: App para projetos práticos
- `users/`: App para gerenciamento de usuários e perfis
- `templates/`: Templates HTML
- `static/`: Arquivos estáticos (CSS, JS, imagens)
- `media/`: Uploads de usuários (avatares, certificados, etc)

## Desenvolvimento

Para contribuir com o projeto, siga estas etapas:

1. Crie uma branch para sua funcionalidade: `git checkout -b feature/nome-da-funcionalidade`
2. Faça suas alterações e commit: `git commit -m 'Adiciona nova funcionalidade'`
3. Envie para o repositório: `git push origin feature/nome-da-funcionalidade`
4. Crie um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT.
