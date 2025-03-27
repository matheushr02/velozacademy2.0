from django import forms
from django.utils.text import slugify
from .models import Curso, Modulo, Aula
import uuid

class CursoForm(forms.ModelForm):
    CONTENT_TYPE_CHOICES = (
        ('texto', 'Somente Texto'),
        ('video', 'Somente Vídeos'),
        ('texto_video', 'Texto e Vídeos'),
        ('anexos', 'Anexos'),
        ('completo', 'Texto, Vídeos e Anexos'),
    )
    
    categoria = forms.CharField(max_length=100, required=True, 
                               help_text="Ex: Python, Java, JavaScript, etc.")
    tipo_conteudo = forms.ChoiceField(choices=CONTENT_TYPE_CHOICES, required=True)
    
    class Meta:
        model = Curso
        fields = ['titulo', 'descricao', 'nivel', 'preco', 'desconto', 'imagem']
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
    video_url = forms.URLField(required=False, help_text="URL do vídeo (Youtube, Vimeo, etc.)")
    conteudo = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    arquivos = forms.FileField(required=False)
    
    class Meta:
        model = Aula
        fields = ['titulo', 'duracao_minutos']
        
    def clean(self):
        cleaned_data = super().clean()
        #? Verifica se pelo menos um dos campos de conteúdo foi preenchido
        if not cleaned_data.get('video_url') and not cleaned_data.get('conteudo') and not cleaned_data.get('arquivos'):
            raise forms.ValidationError('Uma aula deve ter pelo menos vídeo, texto ou arquivos.')
        return cleaned_data