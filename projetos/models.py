from django.db import models
from django.urls import reverse

class Tecnologia(models.Model):
    nome = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = 'Tecnologia'
        verbose_name_plural = 'Tecnologias'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome

class Projeto(models.Model):
    DIFICULDADE_CHOICES = (
        ('facil', 'Fácil'),
        ('medio', 'Médio'),
        ('dificil', 'Difícil'),
    )
    
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    descricao = models.TextField()
    objetivo = models.TextField()
    imagem = models.ImageField(upload_to='projetos/', blank=True, null=True)
    dificuldade = models.CharField(max_length=10, choices=DIFICULDADE_CHOICES, default='medio')
    tecnologias = models.ManyToManyField(Tecnologia, related_name='projetos')
    tempo_estimado_horas = models.PositiveIntegerField(default=10)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('projetos:detalhe', args=[self.id])

class Etapa(models.Model):
    projeto = models.ForeignKey(Projeto, related_name='etapas', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    instrucoes = models.TextField()
    ordem = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['ordem']
        verbose_name = 'Etapa'
        verbose_name_plural = 'Etapas'
    
    def __str__(self):
        return f"{self.titulo} - {self.projeto.titulo}"
