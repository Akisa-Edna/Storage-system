from decimal import Decimal
#the prices for luggage transportation
PICKUP_PRICE = Decimal(350.00)  
LORRY_PRICE = Decimal(600.00)  


# transportation/constants.py
SUBCOUNTIES_AND_RATES = {
    'Mvita': {'pickup': (200.00), 'lorry': (350.00)},
    'Jomvu': {'pickup': (300.00), 'lorry': (450.00)},
    'Changamwe': {'pickup': (600.00), 'lorry': (850.00)},
    'Kisauni': {'pickup': (400.00), 'lorry': (550.00)},
    'Nyali': {'pickup': (400.00), 'lorry': (550.00)},
    'Likoni': {'pickup': (500.00), 'lorry': (650.00)},
    # Add more subcounties and rates as needed
}

schools_list = [
    "TUM",
    "KCNP",
    "KMTC",
    "KU",
    # Add more schools as needed
]
