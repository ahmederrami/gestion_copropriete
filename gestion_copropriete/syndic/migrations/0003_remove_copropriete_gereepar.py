# Generated by Django 3.1.3 on 2020-11-14 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('syndic', '0002_auto_20201114_0854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='copropriete',
            name='gereePar',
        ),
    ]
