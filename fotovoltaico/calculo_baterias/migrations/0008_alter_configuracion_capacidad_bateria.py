# Generated by Django 5.1.3 on 2024-11-28 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculo_baterias', '0007_rename_eficiencia_sistema_configuracion_eficiencia_bateria_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracion',
            name='capacidad_bateria',
            field=models.FloatField(default=250.0, help_text='Capacidad de baterías (Ah)'),
        ),
    ]