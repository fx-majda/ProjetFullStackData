# Generated by Django 3.1.7 on 2021-03-24 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enqueteur', '0013_auto_20210324_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enqueteur',
            name='profile_pic',
            field=models.FileField(blank=True, default='enqueteur/static/dist/img/AdminLTELogo.png', upload_to=''),
        ),
    ]