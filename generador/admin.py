from django.contrib import admin
from .models import Contrato

@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'requiere_aval', 'cuota_mantenimiento', 'fecha_creacion')
    list_filter = ('requiere_aval', 'cuota_mantenimiento', 'fecha_creacion')
    search_fields = ('nombre',)
    ordering = ('-fecha_creacion',)
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ('fecha_creacion',)
