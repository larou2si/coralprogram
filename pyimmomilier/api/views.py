import datetime
from django.db.models import Q, F, ExpressionWrapper, DecimalField, CharField, Value
from django.db.models.functions import Concat
from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import Appartement, Caracteristique, Programme

# Create your views here.

# -------------------------- Tache 1 ------------------------
class MyProgs(generics.ListAPIView):
    """ this API will retrieve all programmes with its relationship.
     it will contain all the data related to its appartements and carateristiques """
    queryset = Programme.objects.all()
    serializer_class = ProgrammeSerializer
# -------------------------- End of Tache 1 ------------------------


# -------------------------- Tache 2 ------------------------
class MyImmobilier(generics.ListCreateAPIView):
    """
    we inherite from generics.ListCreateAPIView to create an 2 APIs in one entrypoint.
    if it is GET request method: we retrieve all the appartements
    if it is a POST method: we create new appartement 
    -> we should validate the data before the insertion. in this case we garante that the appartement must be affeted to program
    as the Appartement Model don't accept a null value in 'program' field
    """
    queryset = Appartement.objects.all()
    serializer_class = AppartementSerializer
# -------------------------- End of Tache 2 ------------------------



# -------------------------- Tache 3 ------------------------
@api_view(['GET'])
def appartement_with_actif_program(request):
    """
    this API accepts only GET method. we fetch all appartement that have an actif program
    """
    appartments = Appartement.objects.filter(program__is_active=True)
    data = AppartementsSerializer(appartments, many=True).data
    return Response(data)


@api_view(['GET'])
def appartement_in_price_range(request):
    """
    this API accepts only GET method. we fetch all appartement in a speciic range of price. default range [100000, 180000]
    """
    min_price = 100000
    max_price = 180000

    # to make this API dynamic to accept the range of price from the user
    if request.GET.get('max_price'):
        max_price = float(request.GET.get('max_price'))
    if request.GET.get('min_price'):
        min_price = float(request.GET.get('min_price'))
    
    if max_price < min_price:
        return Response({"invalid": "Price range is invalid!"}, status=400)

    # we fetch the date in the range of price
    #appartments = Appartement.objects.filter(prix__range=(min_price, max_price))
    appartments = Appartement.objects.filter(Q(prix__gte=min_price), Q(prix__lte=max_price))

    data = AppartementsSerializer(appartments, many=True).data
    return Response(data)

@api_view(['GET'])
def programs_has_piscine(request):
    """
    this API accepts only GET method. we fetch all programs that has at least an appartement contains a piscine as a caracteristque
    """
    programs = Programme.objects.filter(Q(apparts__caracteristiques__name='piscine')).distinct()
    # if we want to verify that at least one of program' appartements has a piscine,
    # we use ProgrammeSerializer which responsable to all programm relationships
    #data = ProgrammeSerializer(programs, many=True).data

    # this serializer return only the program fields
    data = ProgrammeSimpleSerializer(programs, many=True).data
    return Response(data)


@api_view(['GET'])
def promo(request):
    """
    this API accepts only GET method. in a compaign we want to provide for our clients some price reduction
    if the code is equal to 'PERE NOEL', we reduce the price by 5% and we set a libelle for our program name
    """
    # if there is a param 'code' in GET request method, we try to fetch it in order to lunch our compaign if the code equal to 'PERE NOEL'
    code = request.GET.get('code')
    if code and str(code).upper()=="PERE NOEL":
        appartments = Appartement.objects.annotate(libelle=Concat(F('program__name') , Value(" PROMO SPECIALE"), output_field=CharField()), promoprice=ExpressionWrapper((F('prix')*0.95), output_field=DecimalField()))
    else:
        appartments = Appartement.objects.annotate(libelle=F('program__name'), promoprice=F('prix') )
    
    #we have to use AppartementPromoSerializer in order to respect the annotated fields added in the queryset
    data = AppartementPromoSerializer(appartments, many=True).data    
    return Response(data)


@api_view(['GET'])
def recommandation(request, date=None):
    """
    this API accepts only GET method. as a recommendation system which depend on the season when the user uses our website

    """

    # we will use this date format : date='10-10-2017'
    try:
        date = datetime.datetime.strptime(date, '%m-%d-%Y')
    except:
        return Response({"invalid": "Date format is invalid, we accept month-day-year like this 10-10-2017 !"}, status=400)

    # to accept the request date as specified in the test description, we this solution
    #if not date:
    #    date = datetime.date.today()
    
    if date.month in [12,1,2,3]:  # [dec, jan, fev, mars]
        has_caracteristic = 'proche station ski'
    elif date.month in [6,7,8,9]: # [juin, july, Aout, Sep]
        has_caracteristic = 'piscine'
    else:
        has_caracteristic = ''
    
    if has_caracteristic=='':
        appartments = Appartement.objects.all().order_by('-prix', '-surface')
    else:
        appartments = Appartement.objects.filter(Q(caracteristiques__name=has_caracteristic))
        appartments2 = Appartement.objects.filter(~Q(caracteristiques__name=has_caracteristic))
        appartments.union(appartments2).order_by('-prix', '-surface')
    data = AppartementSerializer(appartments, many=True).data 
    return Response(data)
# -------------------------- End ofTache 3 ------------------------


# this an extra work!
def dashboard(request):
    """
    try to create HTML page to display some graphics:
        - nombre d'appatement par mois
        - l'evolution des prix au cours du temps, si on ajoute date au model appartement....
        - l'evolution des prix par rapport à la surface
    """
    return render()