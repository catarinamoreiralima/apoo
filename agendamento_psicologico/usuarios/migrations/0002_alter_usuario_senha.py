# Generated by Django 5.1 on 2024-12-12 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='senha',
            field=models.CharField(max_length=128),
        ),
    ]
