from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
import datetime

# Create your models here.

class User(AbstractUser):
    def getProprietes(self):
        result=[]
        for prop in self.proprietaires.filter(actif=True):
            result = result+list(prop.partiesPrivees.all())
        return result
    def getCoproprietesGerees(self):
        result=[]
        for gest in self.gestionnaires.filter(actif=True):
            result = result+list(gest.coproprietes.all())
        return result

class Copropriete(models.Model):
    copropriete = models.CharField(max_length = 200)
    adresse = models.CharField(max_length = 200)
    ville = models.CharField(max_length = 50)
    pays = models.CharField(max_length = 50)
    totalPartsCopropriete = models.DecimalField(max_digits=10, decimal_places = 2)
    creeLe = models.DateTimeField(auto_now_add = True)
    modifieLe = models.DateTimeField(auto_now = True)
    actif = models.BooleanField(default = False)

    class Meta:
        unique_together = [['copropriete', 'ville']]

    def __str__(self):
        return f'{self.copropriete}, {self.ville}, {self.pays}'
    
    def totalPartsExact(self):
        sumPartsDansCopropriete = sum(pdc.partDansCopropriete for pdc in self.partiesPrivees.all())
        if sumPartsDansCopropriete == self.totalPartsCopropriete:
            return True
        else:
            return False

    def getCoproprietairesActuels(self):
        result = []
        for pp in self.partiesPrivees.filter(actif=True):
            for proprietaire in pp.hist_proprietaires.filter(actif=True):
                result.append(proprietaire.proprietaire)
        return list(set(result))

    def getGestionairesActuels(self):
        return self.hist_gestionnaires.filter(actif=True)
    
    def getSituationFinanciere(self,annee):
        result={}
        for compte in self.comptes.filter(actif=True):
            result[compte.libelle_compte]=compte.solde_compte()
        return result
    
    def getJournalTransactions(self,annee):
        return self.transactions.filter(date_comptable__year=annee)

    def cloturerExercice(self,exercice): #normalement exercice precedent
        pass
        #condition : on est sur le nouveau exercice (exercice+1), ecriture de cloture non encore passee
        #procedure : calculer le solde CPC, passer l'ecriture resultat-exercice-cpc avec resultat-exercice-bilan

    def ouvrirExercice(self,exercice):
        pass
        #procedure : s'assuer que le bilan est equilibre, passer les soldes des comptes de bilan de 
        #l'exercice precedent avec le solde initial
 

class Parametre(models.Model):
    copropriete = models.OneToOneField(Copropriete, on_delete = models.CASCADE,primary_key=True, related_name="parametres")
    exerciceOuvert = models.IntegerField(blank=False, null=False)
    cotisationMensuelle = models.DecimalField(max_digits=10, decimal_places=2)
    creeLe = models.DateTimeField(auto_now_add = True)
    modifieePar = models.ForeignKey(User, on_delete = models.CASCADE)
    modifieLe = models.DateTimeField(auto_now = True)

class PartiePrivee(models.Model):
    copropriete = models.ForeignKey(Copropriete, on_delete = models.CASCADE, related_name = "partiesPrivees")
    identifiant = models.CharField(max_length = 200)
    partDansCopropriete = models.DecimalField(max_digits=10, decimal_places = 2)
    creeLe = models.DateTimeField(auto_now_add = True)
    modifieLe = models.DateTimeField(auto_now = True)
    actif = models.BooleanField(default = True)

    class Meta:
        unique_together = [['copropriete', 'identifiant']]

    def __str__(self):
        return f'{self.copropriete.copropriete}, {self.identifiant}'

    def getProprietairesActuels(self):
        return self.hist_proprietaires.filter(actif=True)

class Proprietaire(models.Model):
    partiesPrivees = models.ManyToManyField(PartiePrivee, related_name = "hist_proprietaires")
    proprietaire = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "proprietaires")
    dateDebut = models.DateTimeField(default=timezone.now)
    dateFin = models.DateTimeField(null=True, blank=True)
    creeLe = models.DateTimeField(auto_now_add = True)
    modifieLe = models.DateTimeField(auto_now = True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.proprietaire.username}'

class Gestionnaire(models.Model):
    ROLE_CHOICES = ( ('President','president'),('Adjoint','adjoint'),('Comptable','comptable'),('Tresorier', 'tresorier'),)
    coproprietes = models.ManyToManyField(Copropriete, related_name = "hist_gestionnaires")
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gestionnaires")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    dateDebut = models.DateTimeField(default=timezone.now)
    dateFin = models.DateTimeField(null=True, blank=True)
    creeLe = models.DateTimeField(auto_now_add = True)
    modifieLe = models.DateTimeField(auto_now = True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.responsable.username}, {self.role}'

class Compte(models.Model): # compte de base a generer automatiquement : caisse, banque, idPP, solde initial,
                            # resultat exercice, resultat-cpc. Les fournisseurs sont a inserer manuellement
    copropriete = models.ForeignKey(Copropriete, on_delete=models.CASCADE, related_name='comptes')
    TYPE_CHOICE = (('Bilan-actif','bilan-actif'), ('Bilan-passif','bilan-passif'),('CPC-Charges', 'cpc-charges'),('CPC-Revenus','cpc-revenus'),)
    type_compte = models.CharField(max_length=20, choices=TYPE_CHOICE)
    libelle_compte = models.CharField(max_length=50)
    creeLe = models.DateTimeField(auto_now_add = True)
    modifieLe = models.DateTimeField(auto_now = True)
    actif = models.BooleanField(default=True)

    class Meta:
        unique_together = [['copropriete', 'type_compte', 'libelle_compte']]

    def __str__(self):
        return f'{self.type_compte},{self.libelle_compte}'
    def total_debit(self):
        return sum(x.montant for x in self.mouvements_debit.all())
    def total_credit(self):
        return sum(x.montant for x in self.mouvements_credit.all())
    def solde_compte(self):
        return self.total_debit()-self.total_credit()
    def desactiver(self):
        if self.solde_compte()==0:
            self.actif=False
            return "Le compte a ete desactive"
        else:
            return "Le compte ne peut etre desactive si son solde n'est pas nul"


class Transaction(models.Model):
    copropriete = models.ForeignKey(Copropriete, on_delete=models.CASCADE, related_name='transactions')
    operation = models.CharField(max_length=200)
    compte_debit = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='mouvements_debit')
    compte_credit = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='mouvements_credit')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    justification = models.FileField(upload_to='justifs/%Y/%m/%d/', blank=False)
    date_comptable = models.DateTimeField(default=timezone.now,blank=False)
    creePar = models.ForeignKey(User, on_delete = models.CASCADE, related_name="transactionsCrees")
    valideePar = models.ForeignKey(User, on_delete = models.CASCADE, related_name="transactionsValidees",null=True)
    creeLe = models.DateTimeField(auto_now_add = True)
    modifieLe = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'{self.operation},{self.compte_debit},{self.compte_credit},{self.montant}'

    def validerDateComptable(self):
        exOuv=self.copropriete.parametres.exerciceOuvert
        if self.date_comptable.year==exOuv:
            return True
        else:
            if self.date_comptable.year>exOuv and self.date_comptable<=timezone.now():
                return True
            else:
                return "Date comptable non valide"