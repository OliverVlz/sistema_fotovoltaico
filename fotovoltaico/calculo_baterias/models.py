from django.db import models

class Electrodomestico(models.Model):
    # Campos del electrodoméstico
    nombre = models.CharField(max_length=100, help_text="Nombre del electrodoméstico")
    cantidad = models.IntegerField(help_text="Cantidad de electrodomésticos", default=1)
    watts = models.FloatField(help_text="Consumo en watts", default=100.0)
    horas_uso = models.FloatField(help_text="Horas de uso por día", default=1.0)
    dias_uso = models.IntegerField(help_text="Días de uso por semana", default=7)
    alimentacion = models.CharField(
        max_length=2,
        choices=[('AC', 'Corriente Alterna'), ('DC', 'Corriente Directa')],
        default='AC',
        help_text="Tipo de alimentación (AC o DC)"
    )
    
    def __str__(self):
        return f"{self.nombre} ({self.get_alimentacion_display()})"

class Configuracion(models.Model):
    dias_autonomia = models.IntegerField(help_text="Días de autonomía", default=3)
    porcentaje_descarga = models.FloatField(help_text="% de descarga", default=60.0)
    sistema_dc = models.FloatField(help_text="Sistema en voltios DC", default=48.0)
    capacidad_bateria = models.FloatField(help_text="Capacidad de baterías (Ah)", default=250.0)
    voltaje_bateria = models.FloatField(help_text="Voltaje de baterías (V)", default=2.0)
    eficiencia_bateria = models.FloatField(help_text="Eficiencia del sistema (%)", default=85.0)
    potencia_modulo = models.FloatField(help_text="Potencia de módulos (W)", default=300.0)
    voltaje_modulo = models.FloatField(help_text="Voltaje de módulos (V)", default=12.0)
    corriente_nominal = models.FloatField(help_text="Corriente nominal de módulos (A)", default=4.0)
    corriente_corta_circuito = models.FloatField(help_text="Corriente de corto circuito (A)", default=4.5)
    potencia_inversor = models.FloatField(help_text="Potencia del inversor (W)", default=4000.0)
    eficiencia_inversor = models.FloatField(help_text="Eficiencia del inversor (%)", default=92.0)
    horas_sol_dia = models.FloatField(help_text="Horas de sol pico por día", default=6.0)
    
    def __str__(self):
        return "Configuración del sistema fotovoltaico"