from django import forms
from django.utils.text import slugify
from .models import Curso, Modulo, Aula
import uuid
import os
from django.core.exceptions import ValidationError

def validate_video_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.mkv', '.webm']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Formato de vídeo não suportado pela plataforma; Apenas MP4, AVI, MOV, WMV, MKV e WEBM.')
    if value.size > 500 * 1024 * 1024: # 500MB
        raise ValidationError('O tamanho do arquivo deve ser menor que 500MB.')

class CursoForm(forms.ModelForm):
    imagem = forms.ImageField(required=False, help_text="Formatos recomendados: JPG, PNG, SVG. Proporção ideal 16:9. Tamanho máximo: 5MB.")
    
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
    
    categoria = forms.CharField(max_length=100, required=True, 
                               help_text="Ex: Python, Java, JavaScript, etc.")
    tipo_conteudo = forms.ChoiceField(choices=CONTENT_TYPE_CHOICES, required=True)
    
    class Meta:
        model = Curso
        fields = ['titulo', 'descricao', 'nivel', 'imagem']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Generate the basic slug from the title
        base_slug = slugify(instance.titulo)
        
        # Check if a course with this slug already exists
        if Curso.objects.filter(slug=base_slug).exists():
            # If it does, append a random string to make it unique
            random_suffix = str(uuid.uuid4())[:6]  # Use first 6 chars of a UUID
            instance.slug = f"{base_slug}-{random_suffix}"
        else:
            instance.slug = base_slug
        
        if commit:
            instance.save()
        
        return instance 
    
class AulaForm(forms.ModelForm):
    video_file = forms.FileField(required=False, validators=[validate_video_extension], help_text="Faça upload de um vídeo (maximo:500MB; formatos aceitos: MP4, AVI, MOV, WMV, MKV ou WEBM)")
    video_url = forms.URLField(required=False, help_text="Cole a URL do vídeo (YouTube, Vimeo, etc.)")
    
    conteudo = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    arquivos = forms.FileField(required=False)
    
    class Meta:
        model = Aula
        fields = ['titulo', 'duracao_minutos', 'video_url']
        
    def clean(self):
        cleaned_data = super().clean()
        #? Verifica se pelo menos um dos campos de conteúdo foi preenchido
        if not cleaned_data.get('video_file') and not cleaned_data.get('conteudo') and not cleaned_data.get('arquivos') and not cleaned_data.get('video_url'):
            raise forms.ValidationError('Uma aula deve ter pelo menos vídeo, texto ou arquivos.')
        return cleaned_data