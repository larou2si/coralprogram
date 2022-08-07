from genericpath import isfile
import json, os
import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from api.models import Programme, Appartement, Caracteristique
from pathlib import Path
from django.conf import settings
class Command(BaseCommand):
    """
    after running the database and ensure that the Models in our project are sucessfully migrated!
    we will use a json file to enrich our DB with some real Data.
    use this cmd in terminal: python* manage.py loaddata
    """

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **kwargs) -> None:
        self.stdout.write("importing data into our database from a json file")

        #cwd = Path(__file__).resolve().parent
        cwd = settings.BASE_DIR
        if os.path.isfile(kwargs['file'][0]):
            file = kwargs['file'][0]
        elif os.path.isfile(os.path.join( cwd, kwargs['file'][0])):
            file = os.path.join( cwd, kwargs['file'][0])
        else:
            raise Exception('please specify a valid file path!')
        
        if Programme.objects.all().count() > 0:
            raise Exception("Database already caontains data! delete them and rerun this cmd")

        try:
            # reading the json file with contextManager
            with open(file) as f:
                json_content = json.load(f)

                # iterate the programs and create new record in each iteration with all appartements that has
                for prog in json_content:
                    p = Programme.objects.create(name=prog['name'], is_active=prog['is_active'])

                    # iterate the list of appartements that are affected to this program
                    for appart in prog['apparts']:
                        app = Appartement.objects.create(surface=appart['surface'],
                                                        prix=appart['prix'],
                                                        nomber_of_pieces=appart['nomber_of_pieces'],
                                                        program=p)
                                            
                        for car in appart['caracteristiques']:
                            # we saerch for the caracteristique in our DB, if it is not found we create it then we add it to appartement
                            # otherwise we affect it the appartement
                            if not Caracteristique.objects.filter(id=car['id']).exists():
                                c = Caracteristique.objects.create(id=car['id'], name=car['name'])
                            else:
                                c = Caracteristique.objects.get(id=car['id'])
                            app.caracteristiques.add(c)
                            app.save()

            self.stdout.write(self.style.SUCCESS('Data well inmported from sample.json!'))

            # file will be close automatically with the contextmanager
        except:
            raise Exception("Enter a valid json file to load program immobilier DATA!")