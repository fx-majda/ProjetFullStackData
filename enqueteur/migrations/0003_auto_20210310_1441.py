# Generated by Django 3.1.7 on 2021-03-10 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enqueteur', '0002_remove_createforms_organisme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact_enqueteur',
            name='feedback_reply',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
