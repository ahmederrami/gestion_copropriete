# Generated by Django 3.1.3 on 2020-12-04 08:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('syndic', '0009_auto_20201201_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compte',
            name='type_compte',
            field=models.CharField(choices=[('Bilan-actif', 'bilan-actif'), ('Bilan-passif', 'bilan-passif'), ('CPC-Charges', 'cpc-charges'), ('CPC-Revenus', 'cpc-revenus')], max_length=20),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date_comptable',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='CopropParametres',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exerciceOuvert', models.IntegerField()),
                ('cotisationMensuel', models.DecimalField(decimal_places=2, max_digits=10)),
                ('creeLe', models.DateTimeField(auto_now_add=True)),
                ('modifieLe', models.DateTimeField(auto_now=True)),
                ('copropriete', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='syndic.copropriete')),
                ('modifieePar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]