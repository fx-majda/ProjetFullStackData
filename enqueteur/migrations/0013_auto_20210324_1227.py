# Generated by Django 3.1.7 on 2021-03-24 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enqueteur', '0012_auto_20210318_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enqueteur',
            name='latitude',
            field=models.DecimalField(decimal_places=6, default=0.1, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='enqueteur',
            name='longitude',
            field=models.DecimalField(decimal_places=6, default=0.1, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='enqueteur',
            name='profile_pic',
            field=models.FileField(blank=True, default='enqueteur/static/dist/img/AdminLTELogo.png', null=True, upload_to=''),
        ),
    ]