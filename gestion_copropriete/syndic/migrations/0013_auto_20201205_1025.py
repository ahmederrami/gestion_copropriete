# Generated by Django 3.1.3 on 2020-12-05 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('syndic', '0012_auto_20201204_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copropparametres',
            name='copropriete',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='parametres', serialize=False, to='syndic.copropriete'),
        ),
    ]
