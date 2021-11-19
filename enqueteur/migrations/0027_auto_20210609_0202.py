# Generated by Django 3.1.7 on 2021-06-09 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enqueteur', '0026_remuneration_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enqueteur',
            name='meilleur',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='enqueteur',
            name='pire',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='enqueteur',
            name='restaurant',
            field=models.CharField(blank=True, choices=[('1', 'Entre 0 et 3'), ('2', 'Entre 3 et 6'), ('3', 'Plus de 6')], max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='enqueteur',
            name='situation',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='enqueteur',
            name='societe',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='remuneration_table',
            name='id_survey',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]