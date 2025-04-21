from django.db import models
from django.urls import reverse

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
    slug = models.SlugField(max_length=200, unique=True)
    descricao = models.TextField()
    nivel = models.CharField(max_length=15, choices=NIVEL_CHOICES, default='iniciante')
    imagem = models.ImageField(upload_to='cursos/', blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('cursos:detalhe', args=[self.slug])

class Trilha(models.Model):
    AREA_CHOICES = (
        ('dados', 'Ciência de Dados'),
        ('dev', 'Desenvolvimento de Software'),
        ('automacao', 'Automação'),
        ('ia', 'Inteligência Artificial'),
    )
    
    nome = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='trilhas/', blank=True, null=True)
    area = models.CharField(max_length=15, choices=AREA_CHOICES)
    total_cursos = models.PositiveIntegerField(default=0)
    total_horas = models.PositiveIntegerField(default=0)
    cursos = models.ManyToManyField(Curso, related_name='trilhas', blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nome']
        verbose_name = 'Trilha'
        verbose_name_plural = 'Trilhas'
        
    def __str__(self):
        return self.nome
        
    def get_absolute_url(self):
        return reverse('cursos:trilha', args=[self.slug])
        
    def atualizar_totais(self):
        """Atualiza os totais de cursos e horas com base nos cursos relacionados."""
        self.total_cursos = self.cursos.count()
        total_horas = 0
        for curso in self.cursos.all():
            for modulo in curso.modulos.all():
                total_horas += modulo.aulas.aggregate(models.Sum('duracao_minutos'))['duracao_minutos__sum'] or 0
        self.total_horas = total_horas // 60  # Converter minutos para horas
        self.save()

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
    video_url = models.URLField(blank=True)
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
        return bool(self.video_file) or bool(self.video_url)
    
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
