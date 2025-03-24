from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
    
    def __str__(self):
        return f"Perfil de {self.user.username}"

class Inscricao(models.Model):
    STATUS_CHOICES = (
        ('ativo', 'Ativo'),
        ('cancelado', 'Cancelado'),
        ('pendente', 'Pendente'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscricoes')
    curso = models.ForeignKey('cursos.Curso', on_delete=models.CASCADE, related_name='inscricoes')
    data_inscricao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')
    progresso = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = ['user', 'curso']
    
    def __str__(self):
        return f"{self.user.username} - {self.curso.titulo}"

@receiver(post_save, sender=User)
def criar_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def salvar_perfil(sender, instance, **kwargs):
    instance.perfil.save()
