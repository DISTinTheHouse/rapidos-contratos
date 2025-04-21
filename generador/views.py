from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from .models import Contrato
from django.core.paginator import Paginator
from django.db.models import Count, Q
from datetime import datetime

def generar_contrato(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        requiere_aval = bool(request.POST.get('requiere_aval'))
        cuota_mantenimiento = bool(request.POST.get('cuota_mantenimiento'))

        contrato = Contrato.objects.create(
            nombre=nombre,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            requiere_aval=requiere_aval,
            cuota_mantenimiento=cuota_mantenimiento
        )

        template = get_template('contrato_template.html')
        html = template.render({'contrato': contrato})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=\"Contrato_{contrato.nombre}.pdf\"'
        pisa.CreatePDF(html, dest=response)
        return response

    # Solo GET: mostrar formulario y últimos contratos
    ultimos_contratos = Contrato.objects.order_by('-fecha_creacion')[:10]
    return render(request, 'formulario.html', {
        'contratos': ultimos_contratos
    })

def descargar_contrato(request, contrato_id):
    contrato = get_object_or_404(Contrato, id=contrato_id)

    template = get_template('contrato_template.html')
    html = template.render({'contrato': contrato})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=\"Contrato_{contrato.nombre}.pdf\"'
    pisa.CreatePDF(html, dest=response)
    return response

def historial_contratos(request):
    query = request.GET.get('q', '')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    contratos = Contrato.objects.all()

    if query:
        contratos = contratos.filter(nombre__icontains=query)

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
    total_aval = Contrato.objects.filter(requiere_aval=True).count()
    total_cuota = Contrato.objects.filter(cuota_mantenimiento=True).count()
    fechas_populares = Contrato.objects.values('fecha_inicio').annotate(total=Count('id')).order_by('-total')[:1]

    return render(request, 'historial.html', {
        'page_obj': page_obj,
        'query': query,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'total_hoy': total_hoy,
        'total_aval': total_aval,
        'total_cuota': total_cuota,
        'fecha_top': fechas_populares[0]['fecha_inicio'] if fechas_populares else None
    })
