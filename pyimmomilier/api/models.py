from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.

class Programme(models.Model):
    name = models.CharField(max_length=255, blank=True, null=False, unique=True)
    is_active = models.BooleanField(blank=True, null=False, default=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Caracteristique(models.Model):
    name = models.CharField(max_length=255, blank=True, null=False, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Appartement(models.Model):
    """
    hypothesis: appartement must have a program
    surface, prix, nomber_of_pieces should not be a negative number
    """
    surface = models.DecimalField(max_digits=5, decimal_places=2,validators=[MinValueValidator(1)], blank=True, null=False)
    prix = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0)], blank=True, null=False)
    nomber_of_pieces = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=False, default=0)
    # un appartement ne peut pas appartenir à deux programme !
    program = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='apparts', blank=True, null=False)
    caracteristiques = models.ManyToManyField('Caracteristique', related_name='caracteristiques')
    objects = models.Manager()

    # sold = DatetimeField...
    def __str__(self):
        return str(self.id)
