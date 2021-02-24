# Generated by Django 3.1.7 on 2021-02-23 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enqueteur', '0003_remove_enqueteur_experience'),
    ]

    operations = [
        migrations.AddField(
            model_name='enqueteur',
            name='profile_pic',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='enqueteur',
            name='habitation',
            field=models.CharField(blank=True, choices=[('1', 'Proprietaire'), ('2', 'Locataire')], max_length=40, null=True),
        ),
    ]
