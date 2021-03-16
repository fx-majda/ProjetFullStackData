# Generated by Django 3.1.7 on 2021-03-13 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enqueteur', '0006_commentaire'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='actualite',
            name='keywords',
        ),
        migrations.AddField(
            model_name='actualite',
            name='categorie',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='enqueteur.categorie'),
            preserve_default=False,
        ),
    ]
