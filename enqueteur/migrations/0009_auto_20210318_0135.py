# Generated by Django 3.1.7 on 2021-03-18 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enqueteur', '0008_enqueteur_verification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enqueteur',
            name='verification',
            field=models.CharField(blank=True, choices=[('1', 'oui'), ('2', 'non')], default=0, max_length=25),
        ),
    ]
