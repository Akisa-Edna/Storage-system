from . import views
from django.urls import path


urlpatterns = [
    path('container_book/', views.Container_booking, name='container_book'),
    path('book_spaces/',views.Book_spaces, name='book_spaces'),
    path('viewcontainer/<int:pk>/', views.ViewContainer, name='viewcontainer'),

    #path('get_rates/', views.get_rates, name='get_rates'),
    path('luggage_collection/<int:booking_id>/', views.LuggageCollection, name='luggage_collection'),
    #path('collect/<int:booking_id>/',views.Collect,name='collect'),
    path('collect/<int:booking_id>/',views.Collect,name='collect'),
    path('confirm_rates/<int:booking_id>/', views.ConfirmRates, name='confirm_rates'),
    

    #path('luggage_collection/<int:pk>/', views.LuggageCollection, name='luggage_collection'),
  #  path('calculate_total/',views.Calculate_book, name='calculate_total'),
]
