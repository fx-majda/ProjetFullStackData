# Generated by Django 3.1.7 on 2021-03-11 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enqueteur', '0005_avergedata'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commentaire',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.TextField()),
                ('commentaire', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='enqueteur.actualite')),
            ],
        ),
    ]
