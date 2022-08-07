from unicodedata import name
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import Programme, Appartement, Caracteristique

from api.serializers import AppartementSerializer


class AppartsTest(TestCase):
    """Test Appartements api"""
    

    @classmethod
    def setUpTestData(self):
        self.client = APIClient()
        self.prog1 = Programme.objects.create(name="Immobiliere Howayda", is_active=True)
        self.prog2 = Programme.objects.create(name="Immobiliere Mahboubine", is_active=False)

        self.c1 =  Caracteristique.objects.create(name='piscine')
        self.c2 =  Caracteristique.objects.create(name='proche station ski')
        self.c3 =  Caracteristique.objects.create(name='jardin')

        self.app1 = Appartement.objects.create(program=self.prog1, surface=55.36, prix=148799.18, nomber_of_pieces=4)
        self.app2 = Appartement.objects.create(program=self.prog1, surface=15.4, prix=18799.18, nomber_of_pieces=2)
        self.app3 = Appartement.objects.create(program=self.prog2, surface=75, prix=137854, nomber_of_pieces=4)
        
        self.app1.caracteristiques.add(self.c1)
        self.app1.caracteristiques.add(self.c2)
        self.app2.caracteristiques.add(self.c2)
        self.app3.caracteristiques.add(self.c1)
        self.app3.caracteristiques.add(self.c3)


    def test_retrieve_apparts(self):
        """Test the creation and retrieving Appartmentes """
        #sample_appart()
        res = self.client.get(reverse('immo:apparts'))
        apparts = Appartement.objects.all().order_by('id')
        serializer = AppartementSerializer(apparts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_appartements_actif(self):
        """
        testing the Api for getting the appartements that its program is actif
        """
        res = self.client.get(reverse('immo:actifappartement'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        for appartement in res.data:
            self.assertEqual(appartement['program']['is_active'], True)

    def test_rangeprice(self):
        """
        testing the Api for getting the appartements in a specific range
        """
        min_price = 90000
        max_price =  200000
        res = self.client.get(reverse('immo:rangeprice'), data={'min_price': min_price, 'max_price': max_price})
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        for appartement in res.data:
            self.assertLess(float(appartement['prix']), max_price)
            self.assertGreater(float(appartement['prix']), min_price)

    def test_rangeprice_error(self):
        """
        testing the Api for getting the appartements in a specific range, but we put max_price < min_price
        """
        min_price = 390000
        max_price =  200000
        res = self.client.get(reverse('immo:rangeprice'), data={'min_price': min_price, 'max_price': max_price})
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_programshaspiscine(self):
        res = self.client.get(reverse('immo:programshaspiscine'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        # todo: to verify that the the program has piscine in one of his appartements
        # we should change the the serialzer of this API until we the full data

    
    def test_promo(self):
        """
            todo:
        """
        res = self.client.get(reverse('immo:promo'), data={'code': 'PERE NOEL'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_recommandation(self):
        """
            todo:
        """
        res = self.client.get(reverse('immo:recommandation', kwargs={'date':'10-10-2017'}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_recommandation_invalid_date(self):
        """
            todo:
        """
        res = self.client.get(reverse('immo:recommandation', kwargs={'date':'15-10-2017'}))
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)