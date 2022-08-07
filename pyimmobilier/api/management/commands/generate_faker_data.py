from django.core.management import BaseCommand
from faker import Faker
from faker.providers import BaseProvider
import random
import json
from api.models import Programme, Appartement, Caracteristique
from rest_framework.test import APIClient
from django.urls import reverse

PROGRAMMES_URL = reverse('immo:progs')


def get_all_programmes():
    """we will get all the programmes in the database using APIClient """
    client = APIClient()
    return client.get(PROGRAMMES_URL).data


class Provider(BaseProvider):
    def get_caracteristiques(self, mylist):
        l = []
        while len(l) < 2:
            element = self.random_element(mylist)
            if element not in l:
                l.append(element)
        return l


class Command(BaseCommand):
    fake = Faker()

    # this is a sample of appartment caracteristics
    Caracteristiques = [
        "proche station ski", "piscine", "jardin", "cave", "parking", "Smart Home Tech",
        "Soundproofing", "Modern Appliances", "Security"
    ]

    def handle(self, *args, **kwargs):
        self.fake.add_provider(Provider)
        for _ in self.Caracteristiques:
            car = Caracteristique.objects.create(name=_)
            self.stdout.write(self.style.SUCCESS(f'program name = {car.name}'))
        
        # we generate 10 programme
        for _ in range(10):
            prog = Programme.objects.create(name=self.fake.unique.company(), is_active=random.choice([True, False]))

            # each program contains 20 appartements
            for __ in range(20):
                appart = Appartement.objects.create(surface=round(random.uniform(50, 120), 2),
                                                    prix=round(random.uniform(80000, 300000), 2),
                                                    nomber_of_pieces=random.randint(1, 5),
                                                    program=prog)

                # we search for 2 random caracteristiques then affect them this appartement
                caracteristiques = Caracteristique.objects.filter(
                    name__in=self.fake.get_caracteristiques(self.Caracteristiques))
                for c in caracteristiques:
                    appart.caracteristiques.add(c)
                    appart.save()
                self.stdout.write(self.style.SUCCESS(f'new appartement created with id={appart.id}'))
        
        # after generating a fake data into our database we will export it in json file 
        # using APIClient we recieve all the data Serialized json in prder to dump it in json file
        json_object = json.dumps(get_all_programmes(), indent=4)
        # Writing to sample.json
        with open("sample.json", "w") as outfile:
            outfile.write(json_object)
