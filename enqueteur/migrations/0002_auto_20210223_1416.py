# Generated by Django 3.1.7 on 2021-02-23 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enqueteur', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enqueteur',
            old_name='addresse',
            new_name='adresse',
        ),
    ]