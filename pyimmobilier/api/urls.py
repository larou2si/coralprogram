from django.urls import path
from .views import *

app_name = 'immo'
urlpatterns = [
        path('', MyProgs.as_view(), name='progs-view'),
        
        # Tache 1: 
        path('progs/', MyProgs.as_view(), name='progs'),

        # Tache 2: list all the appartements
        path('apparts/', MyImmobilier.as_view(), name='apparts'),

        # Tache 3:
        path('actifappartement/', appartement_with_actif_program, name='actifappartement'),
        path('rangeprice/', appartement_in_price_range, name='rangeprice'),
        path('programshaspiscine/', programs_has_piscine, name='programshaspiscine'),
        path('promo/', promo, name='promo'), 
        path('recommandation/<str:date>/', recommandation, name='recommandation'), 

        #path('', dashboard, name='dashboard'),

    ]