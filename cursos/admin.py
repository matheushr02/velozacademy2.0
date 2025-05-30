from django.contrib import admin
from .models import Curso, Modulo, Aula, ArquivoAula, Trilha

# Register your models here.
#admin.site.register(Trilha)

#!terminar de criar o admin outro momento
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'nivel', 'publicado', 'data_criacao')
    list_filter = ('publicado', 'categoria', 'nivel', 'is_free', 'data_criacao')
    search_fields = ('titulo', 'descricao', 'categoria')
    prepopulated_fields= {'slug': ('titulo',)}
    fieldsets = (
        (None, {
            'fields': ('titulo', 'slug', 'descricao', 'categoria', 'nivel', 'imagem')
        }),
        ('Publicação', {
            'fields': ('publicado', 'is_free')
        }),
    )
    pass
@admin.register(Trilha)
class TrilhaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'publicada', 'data_criacao', 'data_atualizacao')
    list_filter = ('publicada',)
    search_fields = ('titulo', 'descricao')
    prepopulated_fields = {'slug': ('titulo',)}
    filter_horizontal = ('cursos',)
    fieldsets = (
        (None, {
            'fields': ('titulo', 'slug', 'descricao', 'imagem_capa', 'publicada')
        }),
        ('Cursos da Trilha', {
            'fields': ('cursos',)
        }),
    )
    pass
class ArquivoAulaInline(admin.TabularInline):
    model = ArquivoAula
    extra = 1
    
@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'modulo', 'ordem', 'duracao_minutos', 'has_video')
    list_filter = ('modulo__curso', 'modulo')
    search_fields = ('titulo', 'conteudo', 'modulo__titulo')
    inlines = [ArquivoAulaInline]
    fieldsets = (
        (None, {
            'fields': ('modulo', 'titulo', 'ordem', 'duracao_minutos')
        }),
        ('Conteúdo', {
            'fields': ('conteudo', 'video_embed_code', 'video_file')
        }),
    )

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'ordem')
    list_filter = ('curso',)
    search_fields = ('titulo', 'descricao', 'curso__titulo')