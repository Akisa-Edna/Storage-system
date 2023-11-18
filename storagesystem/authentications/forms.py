from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.db import transaction
from .models import Student, CustomUser,storageProvider,Profile
from django.core.exceptions import ValidationError
from .configstaff import ALLOWED_STAFF_NUMBERS, STAFF_NUMBER_RANGE

class StudentSignUpForm(UserCreationForm):
    first_name=forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter firstname'}))
    last_name=forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter lastname'}))
    email=forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Enter your email'}))
    phone_number=forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter phonenumber'}))
    username=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'confirm password'}))
   
  
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        #added for trying 
        #fields = ['email', 'username', 'password1', "password2","phone"]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.email=self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        student = Student.objects.create(user=user)
        student.phone_number=self.cleaned_data.get('phone_number')

        student.save()
        return user


class storageProviderSignUpForm(UserCreationForm):
   
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}))
    staff_no = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter staff number'}))

    
  
    class Meta(UserCreationForm.Meta):
        model = CustomUser
       # fields = ['email', 'username', 'password1', 'password2', 'phone_number','first_name', 'last_name']  

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.is_storageProvider = True
        user.save()
        storageprovider = storageProvider.objects.create(user=user)
        storageprovider.phone_number=self.cleaned_data.get('phone_number')
        storageprovider.staff_no=self.cleaned_data.get('staff_no')
        
        storageprovider.save()

        return user
    
    def clean_staff_no(self):
        staff_no = self.cleaned_data.get('staff_no')

        # Check if staff number is in the allowed list
        if staff_no not in ALLOWED_STAFF_NUMBERS:
            raise ValidationError('Invalid staff number. Please enter a valid staff number.')

        # Check if staff number is within the specified range
        if not (STAFF_NUMBER_RANGE[0] <= int(staff_no) <= STAFF_NUMBER_RANGE[1]):
            raise ValidationError('Invalid staff number. Please enter a valid staff number within the allowed range.')

        return staff_no
    

class LoginForm(AuthenticationForm):
   
    class Meta:
       fields = ['email', 'password']

class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'old password'}))
        new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'new password'}))
        new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'new password'}))

        model = CustomUser
        fields = ['old_password','new_password1','new_password2']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email','first_name','last_name']