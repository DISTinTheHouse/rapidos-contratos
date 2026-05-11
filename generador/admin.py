from django.contrib import admin
from .models import Contrato

@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'empresa_cliente', 'fecha_inicio', 'fecha_fin', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    search_fields = ('nombre', 'empresa_cliente')
    ordering = ('-fecha_creacion',)
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ('fecha_creacion',)
