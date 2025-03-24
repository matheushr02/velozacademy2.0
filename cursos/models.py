from django.db import models
from django.urls import reverse

class Curso(models.Model):
    NIVEL_CHOICES = (
        ('iniciante', 'Iniciante'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
    )
    
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    descricao = models.TextField()
    nivel = models.CharField(max_length=15, choices=NIVEL_CHOICES, default='iniciante')
    imagem = models.ImageField(upload_to='cursos/', blank=True, null=True)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    desconto = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('cursos:detalhe', args=[self.id])

    def preco_com_desconto(self):
        return self.preco - self.desconto

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
    conteudo = models.TextField()
    ordem = models.PositiveIntegerField(default=0)
    duracao_minutos = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordem']
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'

    def __str__(self):
        return f'{self.titulo} ({self.modulo.titulo})'
