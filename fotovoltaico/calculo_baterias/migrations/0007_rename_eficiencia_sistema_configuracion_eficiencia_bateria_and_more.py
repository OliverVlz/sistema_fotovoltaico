# Generated by Django 5.1.3 on 2024-11-28 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculo_baterias', '0006_remove_configuracion_tension_sistema'),
    ]

    operations = [
        migrations.RenameField(
            model_name='configuracion',
            old_name='eficiencia_sistema',
            new_name='eficiencia_bateria',
        ),
        migrations.AddField(
            model_name='configuracion',
            name='voltaje_bateria',
            field=models.FloatField(default=2.0, help_text='Voltaje de baterías (V)'),
        ),
    ]