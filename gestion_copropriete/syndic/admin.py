from django.contrib import admin
from .models import User, Copropriete, PartiePrivee, Proprietaire, Gestionnaire, Compte, Transaction

# Register your models here.
admin.site.register(User)
admin.site.register(Copropriete)
admin.site.register(PartiePrivee)
admin.site.register(Proprietaire)
admin.site.register(Gestionnaire)
admin.site.register(Compte)
admin.site.register(Transaction)