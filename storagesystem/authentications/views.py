from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,get_user_model,authenticate
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse
from .forms import StudentSignUpForm,storageProviderSignUpForm,LoginForm,UserUpdateForm,ProfileUpdateForm
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser,Student
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .models import StaffNumber
from .utils import release_staff_number
import random

# Create your views here.
def Index(request):
    return render(request,'authentications/index.html')

def SignUp(request):
	return render(request,'authentications/register.html')



class StudentSignUpView(CreateView):
    model = CustomUser
    form_class = StudentSignUpForm
    template_name = 'authentications/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
      
        user = form.save()
        login(self.request, user)
        #sending email to user that just created an account
        subject = 'Welcome to storage facility'
        message = 'Hello {user.first_name} We are glad you are here, you can make your bookings to store your luggage with us.Hopefully we will offer the best services to you.'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
         )

        return redirect('user_login')
    
       

class storageProviderSignUpView(CreateView):
    model = CustomUser
    form_class = storageProviderSignUpForm
    template_name = 'authentications/signupstorage.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'storageprovider'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        #send email once account is created
        subject = 'Welcome to storage facility'
        message = 'Hello {user.first_name}. We are glad you are here, may you provide the best services to our customers.'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
         )

        return redirect('user_login')

   
def get_next_available_staff_number():
    try:
        staff_number = StaffNumber.objects.filter(is_in_use=False).first()
        if staff_number:
            staff_number.is_in_use = True
            staff_number.save()
            return staff_number.number
        else:
            return None  # No available staff numbers
    except StaffNumber.DoesNotExist:
        return None
    
def release_staff_number_view(request, number):
    result = release_staff_number(number)

    if result:
        # Successfully released the staff number
        return redirect('success_page')  # Redirect to a success page
    else:
        # Staff number not found or other error
        return redirect('error_page')  # Redirect to an error page
   

class Login(LoginView):
    form_class=LoginForm #addedline
    template_name = 'authentications/login.html'  

    def get_success_url(self):
       
        
        user = self.request.user
        if user.is_student:
            return reverse('container_book') #same as return redirect
        elif user.is_storageProvider:
            return reverse('dashboard')
        else:
            
            return ('index')  
        
def Logout(request):
    logout(request)
    messages.success(request,'You have been logged out')
    return redirect('index')
            

    


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'authentications/change_password.html', {
        'form': form
    })



def Profile(request):
    if request.method == 'POST':
         
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'authentications/profile.html',context)