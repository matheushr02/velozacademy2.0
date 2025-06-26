from django.contrib import admin
from .models import Perfil, Inscricao

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo_usuario', 'data_assinatura')
    list_filter = ('tipo_usuario',)
    search_fields = ('user__username', 'user__email',)

class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('user', 'curso', 'status', 'data_inscricao', 'progresso')
    list_filter = ('status',)
    search_fields = ('user__username', 'curso__titulo',)
    
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Inscricao, InscricaoAdmin)