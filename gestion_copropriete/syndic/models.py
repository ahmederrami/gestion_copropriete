from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Copropriete(models.Model):
    copropriete = models.CharField(max_length = 200)
    adresse = models.CharField(max_length = 200)
    ville = models.CharField(max_length = 50)
    pays = models.CharField(max_length = 50)
    totalPartsCopropriete = models.DecimalField(max_digits=10, decimal_places = 2)
    creeLe = models.DateTimeField(auto_now_add = True)
    modifieLe = models.DateTimeField(auto_now = True)
    actif = models.BooleanField(default = False)

    def __str__(self):
        return f'{self.copropriete}, {self.ville}, {self.pays}'
    
    def totalPartsExact(self):
        sumPartsDansCopropriete = sum(pdc.PartDansCopropriete for pdc in self.partiesPrivees)
        if sumPartsDansCopropriete == self.totalPartsCopropriete:
            return True
        else:
            return False

    def getCoproprietairesActuels(self):
        result = []
        for pp in self.partiesPrivees.filter(actif=True):
            result = result + pp.proprietaireActuel
        return list(set(result))

    def getGestionairesActuels(self):
        return self.hist_gestionnaires.filter(actif=True)

class PartiePrivee(models.Model):
    copropriete = models.ForeignKey(Copropriete, on_delete = models.CASCADE, related_name = "partiesPrivees")
    identifiant = models.CharField(max_length = 200)
    partDansCopropriete = models.DecimalField(max_digits=10, decimal_places = 2)
    creeLe = models.DateTimeField(auto_now_add = True)
    modifieLe = models.DateTimeField(auto_now = True)
    actif = models.BooleanField(default = True)

    def __str__(self):
        return f'{self.identifiant}'

    def getProprietairesActuels(self):
        return self.hist_proprietaires.filter(actif=True)

class Proprietaire(models.Model):
    partiesPrivees = models.ManyToManyField(PartiePrivee, related_name = "hist_proprietaires")
    proprietaire = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "proprietaires")
    dateDebut = models.DateTimeField()
    dateFin = models.DateTimeField(null=True, blank=True)
    creeLe = models.DateTimeField(auto_now_add = True)
    modifieLe = models.DateTimeField(auto_now = True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.proprietaire.username}'

class Gestionnaire(models.Model):
    ROLE_CHOICES = ( ('President','president'),('Adjoint','adjoint'),('Comptable','comptable'),('Tresorier', 'tresorier'),)
    coproprietes = models.ManyToManyField(Copropriete, related_name = "hist_gestionnaires")
    responsable = models.ForeignKey(User, on_delete = models.CASCADE, related_name="gestionnaires")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    dateDebut = models.DateTimeField()
    dateFin = models.DateTimeField(null=True, blank=True)
    creeLe = models.DateTimeField(auto_now_add = True)
    modifieLe = models.DateTimeField(auto_now = True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.responsable.username}, {self.role}'

class Compte(models.Model):
    copropriete = models.ForeignKey(Copropriete, on_delete=models.CASCADE, related_name='comptes')
    TYPE_CHOICE = (('Bilan-actif','bilan-actif'), ('Bilan-passif','bilan-passif'),('Charges', 'charges'),('Revenus','revenus'),)
    type_compte = models.CharField(max_length=20, choices=TYPE_CHOICE)
    libelle_compte = models.CharField(max_length=50)
    creeLe = models.DateTimeField(auto_now_add = True)
    modifieLe = models.DateTimeField(auto_now = True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.type_compte},{self.libelle_compte}'

class Transaction(models.Model):
    copropriete = models.ForeignKey(Copropriete, on_delete=models.CASCADE, related_name='transactions')
    operation = models.CharField(max_length=200)
    compte_debit = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='mouvements_debit')
    compte_credit = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='mouvements_credit')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    justification = models.FileField(upload_to='justifs/%Y/%m/%d/', blank=False)
    creePar = models.ForeignKey(User, on_delete = models.CASCADE, related_name="transactionsCrees")
    valideePar = models.ForeignKey(User, on_delete = models.CASCADE, related_name="transactionsValidees")
    creeLe = models.DateTimeField(auto_now_add = True)
    modifieLe = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'{self.operation},{self.compte_debit},{self.compte_credit},{self.montant}'