from django.test import TestCase
from syndic.models import User, Copropriete, Parametre, PartiePrivee, Proprietaire, Gestionnaire, Compte, Transaction

class ProprietaireTestCase(TestCase):
    def setUp(self):
        copropriete1=Copropriete.objects.create(copropriete='raison sociale1', adresse='adresse', ville='ville', pays='pays', totalPartsCopropriete=7.0)
        copropriete1.save()
        pp1=PartiePrivee.objects.create(copropriete=copropriete1, identifiant='identifiant1', partDansCopropriete=1.0)
        pp1.save()
        pp2=PartiePrivee.objects.create(copropriete=copropriete1, identifiant='identifiant2', partDansCopropriete=2.0)
        pp2.save()
        pp3=PartiePrivee.objects.create(copropriete=copropriete1, identifiant='identifiant4', partDansCopropriete=4.0)
        pp3.save()
        proprietaire1=Proprietaire.objects.create(username='omar',password='12345678',partiePrivee=pp1)
        proprietaire2=Proprietaire.objects.create(username='chaymae',password='12345678',partiePrivee=pp2)
        proprietaire3=Proprietaire.objects.create(username='ahmed',password='12345678',partiePrivee=pp3)
        proprietaire1.save()
        proprietaire2.save()
        proprietaire3.save()

    def test_user(self):
        proprietaire=Proprietaire.objects.get(username='omar')
        self.assertEqual(proprietaire.password, '12345678')