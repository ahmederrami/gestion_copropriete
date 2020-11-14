from django.contrib import admin
from .models import Copropriete, PartiePrivee, Proprietaire, Gestionnaire

# Register your models here.
admin.site.register(Copropriete)
admin.site.register(PartiePrivee)
admin.site.register(Proprietaire)
admin.site.register(Gestionnaire)