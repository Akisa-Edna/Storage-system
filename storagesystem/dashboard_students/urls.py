from . import views
from django.urls import path
#from .views import LNMCallbackUrlAPIView


urlpatterns = [
    path('container_book/', views.Container_booking, name='container_book'),
    path('book_spaces/',views.Book_spaces, name='book_spaces'),
    #path('book',views.Book,name='book'),
    path('viewcontainer/<int:pk>/', views.ViewContainer, name='viewcontainer'),

    
    path('luggage_collection/<int:booking_id>/', views.LuggageCollection, name='luggage_collection'),
    path('payment/<int:booking_id>/',views.payment,name='payment'),
   # path('complete', views.complete, name='complete'),
   # path("lnm/", LNMCallbackUrlAPIView.as_view(), name="lnm-callbackurl"),
    path('contact',views.Contact,name='contact'),
    
]
