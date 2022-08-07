import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    this cmd should be used when we are trying to deploy our APP within docker image!
    before the start of our Django project we must pause its execution until database become available
    use this cmd in terminal: python* manage.py loaddata
    """

    def handle(self, *args, **kwargs) -> None:
        self.stdout.write("Waiting for database")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unvailble, waiting 1 second ...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))
