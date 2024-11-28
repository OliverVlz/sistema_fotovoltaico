from django import forms
from .models import *

class ElectrodomesticoForm(forms.ModelForm):
    class Meta:
        model = Electrodomestico
        fields = ['nombre', 'cantidad' ,'watts', 'horas_uso', 'dias_uso', 'alimentacion']

class ConfiguracionForm(forms.ModelForm):
    class Meta:
        model = Configuracion
        fields = '__all__'