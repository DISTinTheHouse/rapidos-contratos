from django.db import models
from datetime import date, timedelta

class Contrato(models.Model):
    MESES_GARANTIA_CHOICES = [
        (3, '3 meses'),
        (6, '6 meses'),
        (12, '12 meses'),
    ]

    VIGENCIA_CHOICES = [
        (15, '15 días'),
        (30, '30 días'),
    ]

    nombre = models.CharField("Nombre del cliente", max_length=100)
    empresa_cliente = models.CharField("Empresa del cliente", max_length=150, blank=True)
    telefono_cliente = models.CharField("Teléfono del cliente", max_length=40, blank=True)
    email_cliente = models.EmailField("Email del cliente", blank=True)
    direccion_cliente = models.CharField("Dirección del cliente", max_length=200, blank=True)
    descripcion = models.TextField("Descripción del servicio", blank=True)
    fecha_inicio = models.DateField("Fecha de inicio", default=date.today)
    fecha_fin = models.DateField("Fecha de fin")
    dias_entrega = models.PositiveIntegerField("Días de entrega", default=30)
    meses_garantia = models.PositiveIntegerField("Meses de garantía", choices=MESES_GARANTIA_CHOICES, default=6)
    vigencia_dias = models.PositiveIntegerField("Días de vigencia", choices=VIGENCIA_CHOICES, default=30)
    monto_total = models.DecimalField("Monto total del servicio", max_digits=12, decimal_places=2, default=0)
    observaciones = models.TextField("Observaciones", blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calcular fecha_fin automáticamente si no está seteada
        if not self.fecha_fin and self.dias_entrega:
            self.fecha_fin = self.fecha_inicio + timedelta(days=self.dias_entrega)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre