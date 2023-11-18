from django.db import models
from django.contrib.auth.models import AbstractUser
from authentications.models import Student 
from django.utils import timezone
import datetime
from .constants import PICKUP_PRICE, LORRY_PRICE





# Create your models here.

    
class Container(models.Model):

    STATUS = [
        ('available','Available'),
        ('occupied','Occupied'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='container_images/')
    price = models.DecimalField(max_digits=6, decimal_places=2,null=0)
    units = models.IntegerField(null=True,blank=True)
    category = models.ManyToManyField('Category',related_name='space')
    status = models.CharField(max_length=100,choices=STATUS)

    #status newcode
    def update_status(self):
        if self.units > 0:
            self.status = 'available'
        else:
            self.status = 'occupied'
        self.save()

    #def __str__(self):
      #  return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 
    
class Booking(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True)
    spaces = models.ManyToManyField('Container',related_name='book')   
    price = models.DecimalField(max_digits=7, decimal_places=2,null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)

    date_booked = models.DateTimeField(default=timezone.now)
    #date_booked = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100,blank=True)
    email = models.CharField(max_length=100,blank=True)
    phonenumber = models.IntegerField(blank=True,null=True)
    county = models.CharField(max_length=100,blank=True)
    subcounty = models.CharField(max_length=100,blank=True)
    school = models.CharField(max_length=100,blank=True,null=True)
    rate = models.DecimalField(max_digits=7, decimal_places=2,null= True)

  

   
    transportation_choice = models.CharField(max_length=100, choices=[('pickup', 'Pick-up'), ('lorry', 'Lorry')], blank=True, null=True)

   # def calculate_total_price(self):
   #     total_price = self.price
    #    if self.transportation_choice == 'pickup':
   #         total_price += PICKUP_PRICE  # Define PICKUP_PRICE as the price for pick-up
   #     elif self.transportation_choice == 'lorry':
    #        total_price += LORRY_PRICE  # Define LORRY_PRICE as the price for lorry
   #     return total_price

   # def save(self, *args, **kwargs):
    #    # Calculate the total price and update the price field
   #     self.price = self.calculate_total_price()
   #     super(Booking, self).save(*args, **kwargs)  -->

    def __str__(self):
        return f'book:{self.date_booked.strftime("%d/%m/%Y, %H:%M:%S")}'





    






