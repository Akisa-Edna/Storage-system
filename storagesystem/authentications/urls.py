from . import views
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import SignUp,StudentSignUpView,storageProviderSignUpView,Login


urlpatterns = [
    path('', views.Index, name='index'),

   # path('signupprevious', views.Signup, name='signup'),
   # path('signin', views.Signin, name='signin'),
   # path('signout', views.Signout, name='signout'),

    
    path('login/', Login.as_view(), name='user_login'),
    path('signup/',views.SignUp,name='signup'),
    path('signup/student/', StudentSignUpView.as_view(), name='student_signup'),
    path('signup/storageProvider/', storageProviderSignUpView.as_view(), name='storageProvider_signup'),
    path('signout',views.Logout,name='signout'),
    path('change_password',views.change_password,name='change_password'),
    path('profile',views.Profile,name='profile'),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="authentications/password_reset.html"),name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="authentications/password_reset_sent.html"),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="authentications/password_reset_confirm.html"),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="authentications/password_reset_complete.html"),name = 'password_reset_complete'),

   # path('profile/<username>',views.profile, name='profile'),
   
]

