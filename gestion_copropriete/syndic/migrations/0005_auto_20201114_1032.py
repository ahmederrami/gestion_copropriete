# Generated by Django 3.1.3 on 2020-11-14 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('syndic', '0004_auto_20201114_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proprietaire',
            name='dateFin',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
