# Generated by Django 3.1.7 on 2021-03-02 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enqueteur', '0004_auto_20210302_1453'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mission',
            old_name='Nom',
            new_name='nom',
        ),
    ]
