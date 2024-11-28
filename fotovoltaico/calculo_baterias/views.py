from .forms import *
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib import messages
import math

def lista_electrodomesticos(request):
    # Obtén o crea la configuración global
    configuracion, created = Configuracion.objects.get_or_create(id=1)

    # Obtén todos los electrodomésticos
    electrodomesticos = Electrodomestico.objects.all()

    # Obtenemos los campos y sus valores dinámicamente para la tabla de configuraciones
    configuracion_data = [
        {
            "help_text": field.help_text,
            "value": getattr(configuracion, field.name)
        }
        for field in Configuracion._meta.fields if field.name != "id"
    ]

    return render(request, 'calculo_baterias/lista_electrodomesticos.html', {
        'electrodomesticos': electrodomesticos,
        'configuracion_data': configuracion_data,
    })

def resultados(request):
    # Obtén o crea la configuración global
    configuracion, created = Configuracion.objects.get_or_create(id=1)

    # Inicializa los valores de consumo
    consumo_diario_AC = 0
    consumo_diario_DC = 0
    watts_AC = 0

    # Obtén todos los electrodomésticos
    electrodomesticos = Electrodomestico.objects.all()

    # Realizar cálculos para cada electrodoméstico
    for e in electrodomesticos:
        if e.alimentacion == 'AC':
            consumo_diario_AC += e.watts * e.horas_uso * e.cantidad
            watts_AC += e.watts * e.cantidad
        else:
            consumo_diario_DC += e.watts * e.horas_uso * e.cantidad

    # Realizar cálculos de dimensionamiento
    # Dimensionamiento de baterías
    a_h_dia = ((consumo_diario_AC / configuracion.eficiencia_inversor) + consumo_diario_DC) / configuracion.sistema_dc
    num_baterias_paralelo = math.ceil((a_h_dia * configuracion.dias_autonomia) / (configuracion.capacidad_bateria * configuracion.porcentaje_descarga))
    num_baterias_serie = math.ceil(configuracion.sistema_dc / configuracion.voltaje_modulo)
    num_total_baterias = math.ceil(num_baterias_paralelo * num_baterias_serie)

    # Dimensionamiento de paneles
    amperes_pico = a_h_dia / (configuracion.eficiencia_bateria * configuracion.horas_sol_dia)
    num_modulos_fotovoltaicos_paralelo = math.ceil(amperes_pico / configuracion.corriente_nominal)
    num_modulos_fotovoltaicos_serie = math.ceil(configuracion.sistema_dc / configuracion.voltaje_modulo)
    num_total_modulos_fotovoltaicos = math.ceil(num_modulos_fotovoltaicos_paralelo * num_modulos_fotovoltaicos_serie)

    # Dimensionamiento de controlador
    capacidad_cortocircuito = math.ceil(1.25 * num_modulos_fotovoltaicos_paralelo * configuracion.corriente_corta_circuito)

    # Preparar los resultados para mostrar en la plantilla
    resultados = {
        'consumo_diario_AC': consumo_diario_AC,
        'consumo_diario_DC': consumo_diario_DC,
        'a_h_dia': round(a_h_dia, 2),
        'num_baterias_paralelo': num_baterias_paralelo,
        'num_baterias_serie': num_baterias_serie,
        'num_total_baterias': num_total_baterias,
        'num_modulos_fotovoltaicos_paralelo': num_modulos_fotovoltaicos_paralelo,
        'num_modulos_fotovoltaicos_serie': num_modulos_fotovoltaicos_serie,
        'num_total_modulos_fotovoltaicos': num_total_modulos_fotovoltaicos,
        'capacidad_cortocircuito': capacidad_cortocircuito,
    }

    # Obtenemos los campos y sus valores dinámicamente para la tabla
    configuracion_data = [
        {
            "help_text": field.help_text,
            "value": getattr(configuracion, field.name)
        }
        for field in Configuracion._meta.fields if field.name != "id"
    ]

    return render(request, 'calculo_baterias/resultados.html', {
        'electrodomesticos': electrodomesticos,
        'resultados': resultados,
        'configuracion_data': configuracion_data,
    })

# Vista para Editar un Electrodoméstico
class EditarElectrodomestico(UpdateView):
    model = Electrodomestico
    form_class = ElectrodomesticoForm
    template_name = 'calculo_baterias/editar_electrodomestico.html'
    success_url = reverse_lazy('lista_electrodomesticos')  # Redirige después de guardar

def agregar_electrodomestico(request):
    if request.method == 'POST':
        form = ElectrodomesticoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Electrodoméstico agregado correctamente.")
            return redirect('lista_electrodomesticos')
    else:
        form = ElectrodomesticoForm()
    return render(request, 'calculo_baterias/agregar_electrodomestico.html', {'form': form})

class EditarElectrodomestico(UpdateView):
    model = Electrodomestico
    form_class = ElectrodomesticoForm
    template_name = 'calculo_baterias/editar_electrodomestico.html'
    success_url = reverse_lazy('lista_electrodomesticos')

def eliminar_electrodomestico(request, pk):
    # Obtén el objeto o devuelve un 404 si no existe
    electrodomestico = get_object_or_404(Electrodomestico, pk=pk)

    # Elimina el electrodoméstico
    electrodomestico.delete()

    # Agrega un mensaje de éxito
    messages.success(request, f'El electrodoméstico "{electrodomestico.nombre}" ha sido eliminado exitosamente.')

    # Redirige a la lista de electrodomésticos
    return redirect('lista_electrodomesticos')

def editar_configuracion(request):
    configuracion, created = Configuracion.objects.get_or_create(id=1)
    if request.method == 'POST':
        form = ConfiguracionForm(request.POST, instance=configuracion)
        if form.is_valid():
            form.save()
            return redirect('lista_electrodomesticos')
    else:
        form = ConfiguracionForm(instance=configuracion)

    return render(request, 'calculo_baterias/editar_configuracion.html', {'form': form})