# Generated by Django 3.1.3 on 2020-12-04 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('syndic', '0010_auto_20201204_0812'),
    ]

    operations = [
        migrations.RenameField(
            model_name='copropparametres',
            old_name='cotisationMensuel',
            new_name='cotisationMensuelle',
        ),
    ]