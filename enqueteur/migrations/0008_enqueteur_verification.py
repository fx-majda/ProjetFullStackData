# Generated by Django 3.1.7 on 2021-03-18 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enqueteur', '0007_auto_20210314_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='enqueteur',
            name='verification',
            field=models.BooleanField(default=False),
        ),
    ]