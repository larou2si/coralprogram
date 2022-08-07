from rest_framework import serializers
from .models import Appartement, Caracteristique, Programme


class ProgrammeSimpleSerializer(serializers.ModelSerializer):
    """Serializer for Programme"""

    class Meta:
        model = Programme
        fields = ('id', 'name', 'is_active')
        read_only_fields = ('id',)


class CaracteristiqueSimpleSerializer(serializers.ModelSerializer):
    """Serializer for Caracteristique"""

    class Meta:
        model = Caracteristique
        fields = ('id', 'name')
        read_only_fields = ('id',)


class AppartementsSimpleSerializer(serializers.ModelSerializer):
    """Serializer for Appartement"""

    class Meta:
        model = Appartement
        fields = ('id', 'surface', 'prix', 'nomber_of_pieces', 'program', 'caracteristiques')
        read_only_fields = ('id',)


# -------------------------- Tache 1 ------------------------
class AppartementsSerializer(serializers.ModelSerializer):
    """ this a customized Serializer for Appartement"""
    program = ProgrammeSimpleSerializer(read_only=True)
    caracteristiques = CaracteristiqueSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Appartement
        fields = ('id', 'surface', 'prix', 'program', 'nomber_of_pieces', 'caracteristiques')
        read_only_fields = ('id',)


class ProgrammeSerializer(serializers.ModelSerializer):
    """this a customized Serializer for Programme, we want to display a program with all his relationships"""
    apparts = serializers.SerializerMethodField()

    class Meta:
        model = Programme
        # depth = 2
        fields = ('id', 'name', 'apparts', 'is_active')
        read_only_fields = ('id',)

    def get_apparts(self, instance):
        """get ordered apparts list"""
        apparts = instance.apparts.all().order_by('id')
        return AppartementsSerializer(apparts, many=True).data


# -------------------------- End Of Tache 1 ------------------------


# -------------------------- Tache 2 ------------------------
class AppartementSerializer(serializers.ModelSerializer):
    """
    this a customized Serializer for Appartement, we want to include the program fields in the appartement fields
    also display the full caracteristiques in a json format
    """
    id_programme = serializers.IntegerField(source='program.id')
    nom_programme = serializers.CharField(source='program.name')
    caracteristiques = CaracteristiqueSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Appartement
        fields = ('id', 'id_programme', 'nom_programme', 'surface', 'prix', 'nomber_of_pieces', 'caracteristiques')
        read_only_fields = ('id',)
# -------------------------- End Of Tache 2 ------------------------
    

# -------------------------- Tache 3 ------------------------
class AppartementPromoSerializer(serializers.ModelSerializer):
    """
    this a customized Serializer for Appartement, we want to include the program fields in the appartement fields
    also display the full caracteristiques in a json format.
    new fields ('libelle_programme', 'price') they are annotated in the queryset
    """
    id_programme = serializers.IntegerField(source='program.id')
    nom_programme = serializers.CharField(source='program.name')
    libelle_programme = serializers.CharField(source='libelle')
    price = serializers.DecimalField(source='promoprice', max_digits=10, decimal_places=2)
    caracteristiques = CaracteristiqueSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Appartement
        fields = ('id', 'id_programme', 'nom_programme', 'libelle_programme', 'surface', 'prix', 'price', 'nomber_of_pieces', 'caracteristiques')
        read_only_fields = ('id',)
# -------------------------- End Of Tache 3 ------------------------
