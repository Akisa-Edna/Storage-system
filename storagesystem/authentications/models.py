from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from PIL import Image #used to resize images uploaded by users


# Create your models here.
class CustomUser(AbstractUser):
  
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    #is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_storageProvider = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Student(models.Model):
    user = models.OneToOneField('CustomUser',null=False, blank=True, on_delete=models.CASCADE,primary_key=True)
    phone_number=models.CharField(max_length=200,null=True)
    

    def __str__(self):
        return self.user.username
    
class storageProvider(models.Model):
    user = models.OneToOneField('CustomUser',null=False, blank=True, on_delete=models.CASCADE,primary_key=True)
    staff_no = models.CharField(max_length=200,null=True)
    phone_number=models.CharField(max_length=200,null=True)
    

    def __str__(self):
        return self.user.username
    
class Profile(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile' 
      
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)   
   
class StaffNumber(models.Model):
    number = models.CharField(max_length=10, unique=True)
    is_in_use = models.BooleanField(default=False)
    

    