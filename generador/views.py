from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from weasyprint import HTML, CSS
from django.http import HttpResponse
from .models import Contrato
from django.core.paginator import Paginator
from django.db.models import Count, Q
from decimal import Decimal
from datetime import datetime

def generar_contrato(request):
    if request.method == 'POST':
        monto_total = Decimal(request.POST.get('monto_total') or '0')
        dias_entrega = int(request.POST.get('dias_entrega') or 30)
        meses_garantia = int(request.POST.get('meses_garantia') or 6)
        vigencia_dias = int(request.POST.get('vigencia_dias') or 30)

        contrato = Contrato.objects.create(
            nombre=request.POST.get('nombre', ''),
            empresa_cliente=request.POST.get('empresa_cliente', ''),
            telefono_cliente=request.POST.get('telefono_cliente', ''),
            email_cliente=request.POST.get('email_cliente', ''),
            direccion_cliente=request.POST.get('direccion_cliente', ''),
            descripcion=request.POST.get('descripcion', ''),
            dias_entrega=dias_entrega,
            meses_garantia=meses_garantia,
            vigencia_dias=vigencia_dias,
            monto_total=monto_total,
            observaciones=request.POST.get('observaciones', '')
        )

        # Cálculos automáticos
        iva = (monto_total * Decimal('0.16')).quantize(Decimal('0.01'))
        subtotal = monto_total
        pago_anticipo = (subtotal * Decimal('0.50')).quantize(Decimal('0.01'))
        pago_avance = (subtotal * Decimal('0.30')).quantize(Decimal('0.01'))
        pago_entrega = (subtotal * Decimal('0.20')).quantize(Decimal('0.01'))
        total_con_iva = (subtotal + iva).quantize(Decimal('0.01'))

        # Fecha de expiración de la vigencia
        from datetime import date, timedelta
        fecha_expiracion = date.today() + timedelta(days=vigencia_dias)

        template = get_template('contrato_template.html')
        html = template.render({
            'contrato': contrato,
            'subtotal': subtotal,
            'iva': iva,
            'pago_anticipo': pago_anticipo,
            'pago_avance': pago_avance,
            'pago_entrega': pago_entrega,
            'total_con_iva': total_con_iva,
            'fecha_expiracion': fecha_expiracion
        })
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=\"Contrato_{contrato.nombre}.pdf\"'

        # Usar WeasyPrint para generar PDF profesional
        HTML(string=html).write_pdf(response)
        return response

    # Solo GET: mostrar formulario y últimos contratos
    ultimos_contratos = Contrato.objects.order_by('-fecha_creacion')[:10]
    return render(request, 'formulario.html', {
        'contratos': ultimos_contratos
    })

def descargar_contrato(request, contrato_id):
    contrato = get_object_or_404(Contrato, id=contrato_id)

    # Cálculos automáticos
    iva = (contrato.monto_total * Decimal('0.16')).quantize(Decimal('0.01'))
    subtotal = contrato.monto_total
    pago_anticipo = (subtotal * Decimal('0.50')).quantize(Decimal('0.01'))
    pago_avance = (subtotal * Decimal('0.30')).quantize(Decimal('0.01'))
    pago_entrega = (subtotal * Decimal('0.20')).quantize(Decimal('0.01'))
    total_con_iva = (subtotal + iva).quantize(Decimal('0.01'))

    # Fecha de expiración de la vigencia
    from datetime import date, timedelta
    fecha_expiracion = date.today() + timedelta(days=contrato.vigencia_dias)

    template = get_template('contrato_template.html')
    html = template.render({
        'contrato': contrato,
        'subtotal': subtotal,
        'iva': iva,
        'pago_anticipo': pago_anticipo,
        'pago_avance': pago_avance,
        'pago_entrega': pago_entrega,
        'total_con_iva': total_con_iva,
        'fecha_expiracion': fecha_expiracion
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=\"Contrato_{contrato.nombre}.pdf\"'

    # Usar WeasyPrint para generar PDF profesional
    HTML(string=html).write_pdf(response)
    return response

def historial_contratos(request):
    query = request.GET.get('q', '')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    contratos = Contrato.objects.all()

    if query:
        contratos = contratos.filter(
            Q(nombre__icontains=query) | Q(empresa_cliente__icontains=query)
        )

    if fecha_inicio:
        contratos = contratos.filter(fecha_creacion__date__gte=fecha_inicio)

    if fecha_fin:
        contratos = contratos.filter(fecha_creacion__date__lte=fecha_fin)

    paginator = Paginator(contratos.order_by('-fecha_creacion'), 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Indicadores tipo dashboard
    hoy = datetime.today().date()
    total_hoy = Contrato.objects.filter(fecha_creacion__date=hoy).count()
    fechas_populares = Contrato.objects.values('fecha_inicio').annotate(total=Count('id')).order_by('-total')[:1]

    return render(request, 'historial.html', {
        'page_obj': page_obj,
        'query': query,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'total_hoy': total_hoy,
        'fecha_top': fechas_populares[0]['fecha_inicio'] if fechas_populares else None
    })
