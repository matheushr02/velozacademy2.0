# Generated by Django 5.0.6 on 2025-05-09 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='data_assinatura',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='perfil',
            name='tipo_usuario',
            field=models.CharField(choices=[('visitante', 'Visitante'), ('estudante', 'VelozEstudante'), ('admin', 'Administrador')], default='visitante', max_length=15),
        ),
    ]
