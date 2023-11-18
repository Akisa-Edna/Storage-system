from . import views
from django.urls import path


urlpatterns = [
     path('dashboard/',views.Dashboard, name='dashboard'),
    # path('container_crud',views.Container_crud,name='container_crud'),

     path('add_booking/', views.AddBooking, name='add_booking'),
     path('update_booking/<int:pk>/',views.UpdateBooking, name='update_booking'),
     path('delete_booking/<str:pk>/',views.DeleteBooking, name='delete_booking'),
     path('view_booking/<int:pk>/', views.ViewBooking, name='view_booking'),

     path('update_container/<int:pk>/',views.UpdateContainer, name='update_container'),
     path('delete_container/<str:pk>/',views.DeleteContainer, name='delete_container'),
     path('view_container/<int:pk>/', views.ViewContainer, name='view_container'),
     path('add_container/', views.AddContainer, name='add_container'),

     #path('search/',views.search,name='search'),
     #path('booking/search/', views.booking_search_view, name='booking_search_view'),
     #path('container/search/', views.container_search_view, name='container_search_view'),


]
