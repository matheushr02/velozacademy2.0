# Generated by Django 5.0.6 on 2025-06-05 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0014_remove_trilha_cursos_old'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trilhacurso',
            options={'ordering': [models.OrderBy(models.F('section_name'), nulls_last=True), 'order'], 'verbose_name': 'Curso na Trilha', 'verbose_name_plural': 'Cursos da Trilha'},
        ),
    ]
