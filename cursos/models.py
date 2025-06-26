from django.db import models
from django.urls import reverse
import os
from django.db.models import F
from django.contrib.auth.models import User
from django.conf import settings

class Curso(models.Model):
    NIVEL_CHOICES = (
        ('iniciante', 'Iniciante'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
    )
    
    CONTENT_TYPE_CHOICES = (
        ('texto', 'Somente Texto'),
        ('video', 'Somente Vídeo'),
        ('texto_video', 'Texto e Vídeo'),
        ('anexos', 'Somente Anexos'),
        ('completo', 'Texto, Vídeo e Anexos'),
        ('texto_anexos', 'Texto e Anexos'),
        ('video_anexos', 'Vídeo e Anexos'),
        ('nenhum', 'Não especificado'),
    )
    
    titulo = models.CharField(max_length=200)
    nivel = models.CharField(max_length=15, choices=NIVEL_CHOICES, default='iniciante')
    slug = models.SlugField(max_length=200, unique=True)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='cursos/', blank=True, null=True, help_text="Imagem de capa para o curso.")
    categoria = models.CharField(max_length=100, default='Indefinido')
    #tipo_conteudo = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default='nenhum')
    publicado = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    is_free = models.BooleanField(default=False, verbose_name="Curso Gratuito")

    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('cursos:detalhe', kwargs={'curso_slug': self.slug})
    
    def get_total_aulas(self):
        count = 0
        for modulo in self.modulos.all():
            count += modulo.aulas.count()
        return count
    
    def get_aulas_concluidas_count(self, user):
        if not user.is_authenticated:
            return 0
        return AulaConcluida.objects.filter(user=user, aula__modulo__curso=self).count()
    
class TrilhaCurso(models.Model):
    trilha = models.ForeignKey('Trilha', on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem")
    section_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Nome da Seção (Opcional)",
        help_text="Ex: Módulo 1, Fundamentos, Avançado"
    )
    
    class Meta:
        ordering = [F('section_name').asc(nulls_last=True), 'order']
        #!Alerta: O uso de unique_together foi depreciado em Django 2.2 e removido em Django 4.0.
        #!Use UniqueConstraint em Meta.constraints para garantir unicidade.
        #? um curso pode estar apenas em uma trilha por vez
        #todo: permitir que o curso esteja em várias trilhas sem restrições
        unique_together = ('trilha', 'curso')
        verbose_name = "Curso na Trilha"
        verbose_name_plural = "Cursos da Trilha"
    
    def __str__(self):
        return f"{self.curso.titulo} na trilha {self.trilha.titulo} (Ordem: {self.order})"

class Trilha(models.Model):
    AREA_CHOICES = (
        ('dados', 'Ciência de Dados'),
        ('dev', 'Desenvolvimento de Software'),
        ('automacao', 'Automação'),
        ('ia', 'Inteligência Artificial'),
    )
    
    titulo = models.CharField(max_length=200, verbose_name="Titulo da Trilha", default="Nova Trilha")
    slug = models.SlugField(max_length=200, unique=True, help_text="Será preenchido automaticamente a partir do título.")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    cursos = models.ManyToManyField(Curso, through='TrilhaCurso', related_name='trilhas_associadas', verbose_name="Cursos na Trilha", blank=True)
    # -removed cursos_old = models.ManyToManyField(Curso, related_name='trilhas_old', blank=True)
    imagem_capa = models.ImageField(upload_to='trilhas_capas/', blank=True, null=True, verbose_name="Imagem de Capa")
    publicada = models.BooleanField(default=False, verbose_name="Publicada")
    area = models.CharField(max_length=15, choices=AREA_CHOICES, blank=True, null=True, verbose_name="Área de Conhecimento")
    #total_cursos = models.PositiveIntegerField(default=0)
    #total_horas = models.PositiveIntegerField(default=0)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['titulo']
        verbose_name = 'Trilha de Aprendizagem'
        verbose_name_plural = 'Trilhas de Aprendizagem'
        
    def __str__(self):
        return self.titulo
        
    def get_absolute_url(self):
        return reverse('cursos:detalhe_trilha', kwargs={'trilha_slug': self.slug})

    #def atualizar_totais(self):
        #"""Atualiza os totais de cursos e horas com base nos cursos relacionados."""
        #self.total_cursos = self.cursos.count()
        #total_horas = 0
        #for curso in self.cursos.all():
            #for modulo in curso.modulos.all():
                #total_horas += modulo.aulas.aggregate(models.Sum('duracao_minutos'))['duracao_minutos__sum'] or 0
        #self.total_horas = total_horas // 60  # Converter minutos para horas
        #self.save()

class Modulo(models.Model):
    curso = models.ForeignKey(Curso, related_name='modulos', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordem']
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'

    def __str__(self):
        return f'{self.titulo} ({self.curso.titulo})'

class Aula(models.Model):
    modulo = models.ForeignKey(Modulo, related_name='aulas', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField(blank=True)
    video_embed_code = models.TextField(blank=True, null=True, verbose_name="Código de Incorporação do Vídeo (iframe)")
    video_file = models.FileField(upload_to='aulas/videos/', blank=True, null=True)
    ordem = models.PositiveIntegerField(default=0)
    duracao_minutos = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordem']
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'

    def __str__(self):
        return f'{self.titulo} ({self.modulo.titulo})'
    
    def has_video(self):
        return bool(self.video_file) or bool(self.video_embed_code and self.video_embed_code.strip())
    
#? Adiciona um novo modelo para os arquivos de aula
class ArquivoAula(models.Model):
    aula = models.ForeignKey(Aula, related_name='arquivos', on_delete=models.CASCADE)
    arquivo = models.FileField(upload_to='aulas/arquivos/')
    nome = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f'Arquivo de {self.aula.titulo}'
    
    def save(self, *args, **kwargs):
        if not self.nome and self.arquivo:
            self.nome = self.arquivo.name
        super().save(*args, **kwargs)

    @property
    def extensao(self):
        if self.arquivo and self.arquivo.name:
            name, extension = os.path.splitext(self.arquivo.name)
            return extension.lstrip('.').upper()
        return ''
    
class AulaConcluida(models.Model):
    #todo para suporte de usuários customizados usar settings.AUTH...
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='aulas_concluidas')
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name='conclusoes')
    data_conclusao = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        unique_together = ('user', 'aula')
        verbose_name = 'Aula Concluída'
        verbose_name_plural = 'Aulas Concluídas'
        
    def __str__(self):
        return f"{self.user.username} concluiu {self.aula.titulo}"