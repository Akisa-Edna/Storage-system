from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from . models import*
from datetime import datetime
import logging
import requests
import base64
import random
from . import keys  
from .forms import BookingForm
from .constants import PICKUP_PRICE, LORRY_PRICE,SUBCOUNTIES_AND_RATES,schools_list
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponse
from requests.auth import HTTPBasicAuth

#mpesa
from mpesa.models import LNMOnline
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .serializers import LNMOnlineSerializer
from datetime import datetime
from rest_framework.response import Response



# Create your views here.
   
#@login_required(login_url='user_login')
def Container_booking(request):
   shared_space = Container.objects.filter(category__name__contains='shared_spaces')
   private_space = Container.objects.filter(category__name__contains='private_spaces')

   context = {
       'shared_spaces': shared_space,
       'private_spaces': private_space,
    }
   
   return render(request,'dashboard_students/book_cont.html',context)


#@login_required(login_url='user_login')                                                      
def Book_spaces(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user  # Get the authenticated user
            if hasattr(user, 'student'):
                student = request.user.student
                name = request.POST.get('name')
                email = request.POST.get('email')
                phonenumber = request.POST.get('phonenumber')
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')
                booking_number = str(random.randint(100000, 999999)) 
         
               
                
                price = 0
                space_ids = []
                

                booking_spaces = {'spaces': []}

                # Get the selected space IDs from the form
                spaces = request.POST.getlist('spaces[]')
                print(spaces)

                if phonenumber:
                     if not (phonenumber.startswith('254') and len(phonenumber) == 12):
                        messages.error(request, "Phone number must start with '254' and have 12 digits.")
                        return render(request, 'dashboard_students/book_cont.html')
   
                else:
                  messages.error(request, "Phone number is required.")
                  return render(request, 'dashboard_students/book_cont.html')   

                 
    

                if start_date and end_date:
                    try:
                        start_date_obj = datetime.fromisoformat(start_date)
                        end_date_obj = datetime.fromisoformat(end_date)
                    except ValueError:
                        messages.error(request, "Invalid date format.")
                        return render(request, 'dashboard_students/book_cont.html')

                    if start_date_obj > end_date_obj:
                        messages.error(request, "End date should be after start date.")
                        return render(request, 'dashboard_students/book_cont.html')

                for space_id in spaces:
                    try:
                      container = Container.objects.get(pk=int(space_id))

                        # Container has available units, proceed with the booking
                      if container.units > 0:
                            # Calculate the number of days
                            start_date_obj = datetime.fromisoformat(start_date)
                            end_date_obj = datetime.fromisoformat(end_date)
                            num_days = (end_date_obj - start_date_obj).days   # Add 1 to include the end date

                            # Use the monthly rate as the space price
                            space_price = container.price  # Assuming container.price represents the monthly rate

                            # Calculate the price based on the number of days
                            if num_days in [30, 31]:
                                mon_price = space_price
                                space_data = {
                                 'id': container.pk,
                                 'name': container.name,
                                 'price': mon_price  # or container.price
                                 }
                                booking_spaces['spaces'].append(space_data)

                                # Decrease the number of units and update status
                                container.units -= 1
                                container.update_status()

                                price += mon_price 
                                space_ids.append(container.pk)
                            else:
                              
                                # Assuming there are 30 or 31 days in a month for simplicity
                              daily_rate = space_price / 30  # Calculate daily rate based on monthly rate
                              individual_price = num_days * daily_rate
                              round_price = round(individual_price, 2)

                              space_data = {
                                 'id': container.pk,
                                 'name': container.name,
                                 'price': round_price#individual_price #or container.price
                              }
                              booking_spaces['spaces'].append(space_data)

                                # Decrease the number of units and update status
                              container.units -= 1
                              container.update_status()

                              price += individual_price  #or container.price
                              space_ids.append(container.pk)

                      else:
                            # Container has 0 units, prevent booking
                            messages.error(request, f"{container.name} is fully booked and unavailable.")

                    except Container.DoesNotExist:
                         print(f"Container with ID {space_id} does not exist.")
                        # Handle the case where a selected space does not exist
                        #pass

                if len(space_ids) > 0:  # Create the booking record only if there are selected spaces
                    # Create the booking record
                    price=sum(space['price'] for space in booking_spaces['spaces']), 
                    print(price)
                    if isinstance(price, tuple):
                         price = price[0] 
                    if isinstance(price, Decimal):
                         numeric_value = price.quantize(Decimal('1.'), rounding='ROUND_HALF_UP')
                         rounded_price = int(numeric_value)
                         print(rounded_price)
    
                    else:
                         rounded_price = price      

                    formatted_price = "{:.2f}".format(rounded_price)
                    print(formatted_price)
                         
                    booking = Booking.objects.create(
                        price=rounded_price, 
                       # price=sum(space['price'] for space in booking_spaces['spaces']),
                        #price=price, 
                        name=name,
                        email=email,
                        phonenumber=phonenumber,
                        start_date=start_date,
                        end_date=end_date,
                        booking_number=booking_number,
                        student=user.student,  # Associate the booking with the student
                    )
                    

                    booking.spaces.add(*space_ids)

                    context = {
                        'booking':booking,
                        'spaces': booking_spaces['spaces'],
                        'price': rounded_price,
                        'booking_id': booking.id  # Include the booking ID for reference
                    }

                    subject = 'Welcome to storage facility'
                    message = f'Hello {name},\n\nYour booking number is {booking.booking_number}. Thank you for booking with us.\n\n The booking period is from {booking.start_date} to {booking.end_date}'
                    send_mail(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False,
                    )


                    return render(request, 'dashboard_students/booking_confirmation.html', context)
                      
                else:
                    # Handle the case where no spaces were selected for booking
                    messages.error(request, "No spaces were selected for booking.")
            
        return render(request, 'dashboard_students/book_cont.html')            
    else:
       return redirect('user_login')


def Contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f"Message from {name}"

        context = {
            'name' : name,
            'email' :email,
            'message' :message
        }

        send_mail(
            subject,
            #name,
            message,
            email,
            ['storagefacilty617@gmail.com'],
            fail_silently=False
        )
       
        
        return render(request,'dashboard_students/contact.html',context)
    else :
        return render(request,'dashboard_students/contact.html')



def ViewContainer(request, pk):
    container = Container.objects.get(id=pk)
    context = {'container': container}
    return render(request, 'dashboard_students/viewcontainer.html', context)




@login_required(login_url='user_login')
def LuggageCollection(request, booking_id):
    # Get the booking based on the booking_id
    
        booking = Booking.objects.get(pk=booking_id)
        schools = schools_list
        subcounties = list(SUBCOUNTIES_AND_RATES.keys())  
        #print(subcounties)
        
        rates = {}  
        selected_subcounty = None
        selected_rate = None 
       # previous_price= booking.price 

        if request.method == 'POST':
            selected_school= request.POST.get('school')
            
            selected_subcounty = request.POST.get('subcounty')
            if selected_subcounty:
                rates = SUBCOUNTIES_AND_RATES.get(selected_subcounty, {})
                selected_rate = request.POST.get('selected_rate') 


            if selected_school and selected_subcounty:
               booking.subcounty = selected_subcounty
               booking.school = selected_school

            


            booking.rate=(selected_rate) 

            if selected_rate is not None:
                previous_price = booking.price if booking.price else Decimal('0')
                total_price = previous_price + Decimal(selected_rate)
                booking.price = total_price 
                booking.save()

                context = {
                   'rates':rates, 
                   'subcounty':selected_subcounty,
                   'rate':selected_rate, 
                   #'total_price':total_price, 
                   'booking':booking,
                   'booking_id':booking_id
                }

                return render(request,'dashboard_students/luggageconfirm.html',context)


            booking.save() 
                
            context = {
                'rates':rates, 
                'subcounty':selected_subcounty,
                'rate':selected_rate, 
                #'total_price':total_price, 
                'booking':booking
            }
            
            
            return render(request, 'dashboard_students/viewrates.html',context) 
        return render(request, 'dashboard_students/luggage_collection.html', {'subcounties': subcounties,'booking':booking,'schools_list':schools})        
       
            

#access_token=''
x=''
def payment(request,booking_id):
    global amount
    global phone
    global date
    booking=Booking.objects.get(pk=booking_id)

    if request.method == 'POST':
          # global access_token 
           name=booking.name
           email = booking.email
           amount = booking.price
           print(amount)
           phone=booking.phonenumber
           print(phone)
       
           if amount is None:
                 return HttpResponse('Amount is required.')
           if phone is None:
                return HttpResponse('Phone number is required.')
        
        
           characters = len(phone)
           value = int(amount)

            # Check if the number of characters in the phone number is greater than or equal to 3
           if characters >= 3:
              check = phone[0] + phone[1] + phone[2]
    
              if check != '254':
                 messages.info(request, 'Your phone number must start with 254 and have 12 characters')
                 return render(request, 'dashboard_students/booking_confirmation.html')
    
              elif characters > 12:
                 messages.info(request, 'Your phone number should not have more than twelve characters')
                 return render(request, 'dashboard_students/booking_confirmation.html')
    
              elif characters < 12:
                 messages.info(request, 'Your phone number should not have less than twelve characters')
                 return render(request, 'dashboard_students/booking_confirmation.html')
    
              elif value < 1:
                 messages.info(request, 'Amount cannot be less than zero')
                 return render(request, 'dashboard_students/booking_confirmation.html')
    
              else:
                       
       

    

                  def generate_access_token():
        
                       consumer_key = keys.consumer_key
                       consumer_secret = keys.consumer_secret
                       api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

                       try:
                           r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
                       except:
                           r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret), verify=False)
        
                       print(r.text)

                       json_response = (
                          r.json()
                        )  

                       my_access_token = json_response["access_token"]

                       return my_access_token

                  generate_access_token()

                  def lipa_na_mpesa():
                      access_token = generate_access_token()
                      global x

          
                      timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                      shortcode = keys.short_code
                       # decoded_password = generate_password(formatted_time)
                      passkey = keys.lipa_na_mpesa_passkey
                      #formatted_time = get_timestamp()
                       #decoded_password = generate_password(formatted_time)
                      stk_password = base64.b64encode((shortcode + passkey + timestamp).encode('utf-8')).decode('utf-8')
                      
    

                      api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
                      #access_token=my_access_token

                      headers = {
                         'Content-Type': 'application/json',
                         'Authorization': 'Bearer %s' % access_token
                       }

                      request = {
                          "BusinessShortCode": keys.business_shortcode,
                           # "Password": decoded_password,
                           "Password": stk_password,
                           "Timestamp": timestamp,
                           "TransactionType": "CustomerPayBillOnline",
                           "Amount": amount,
                           "PartyA": phone,
                           "PartyB": keys.business_shortcode,
                           "PhoneNumber": phone,
                           "CallBackURL": "https://a45c-197-232-90-116.ngrok-free.app/api/payments/lnm/",
                           "AccountReference": "STORAGE",
                           "TransactionDesc": "Pay for spaces booked",
                        }

                      response = requests.post(api_url, json=request, headers=headers)

                      print(response.text)
                      data1=response.json()
                      x=data1['CheckoutRequestID']
                      return x
             
                  lipa_na_mpesa()

              #lipa_na_mpesa()  

  
              context= {
                  'booking_id':booking_id,
                   'booking':booking
                }
              subject = 'Welcome to storage facility'
              message = f'Hello {name},\n\nYour booking number is {booking.booking_number}. Thank you for booking with us.\n\n The booking period is from {booking.start_date} to {booking.end_date}'
              send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
              )




              messages.info(request, 'Check your phone to complete the transaction ')
            
              return render(request,'dashboard_students/payment.html',context) 
           
           else:
                 messages.info(request, 'Phone number incorrect')
                 return render(request, 'dashboard_students/booking_confirmation.html')   
    return render(request,'dashboard_students/booking_confirmation.html')       



'''class LNMCallbackUrlAPIView(CreateAPIView):
    queryset = LNMOnline.objects.all()
    serializer_class = LNMOnlineSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        print(request.data, "this is request.data")


        ''   
          {'Body':
            {'stkCallback':
             {
                'CheckoutRequestID': 'ws_CO_20112023114435271746003536',
                'MerchantRequestID': '12631-12684913-1',
                'ResultCode': 1037,
                'ResultDesc': 'The service request is processed successfully.',
                'CallbackMetadata': {
                                        'Item': [
                                                {'Name': 'Amount', 'Value': 1.0},
                                                {'Name': 'MpesaReceiptNumber', 'Value': 'NCB1FW1DFZ'},
                                                {'Name': 'Balance'},
                                                {'Name': 'TransactionDate', 'Value': 20231111190244},
                                                {'Name': 'PhoneNumber', 'Value': 254746003536}
                                                ]
                                    }

                                    }
                }
            }
        ''


        merchant_request_id = request.data["Body"]["stkCallback"]["MerchantRequestID"]
        print(merchant_request_id, "this should be MerchantRequestID")
        checkout_request_id = request.data["Body"]["stkCallback"]["CheckoutRequestID"]
        result_code = request.data["Body"]["stkCallback"]["ResultCode"]
        result_description = request.data["Body"]["stkCallback"]["ResultDesc"]

        amount = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
        print(amount, "this should be an amount")

        mpesa_receipt_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"]
        print(mpesa_receipt_number, "this should be an mpesa_receipt_number")

        balance = ""

        transaction_date = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][3]["Value"]
        print(transaction_date, "this should be an transaction_date")

        phone_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][ 4 ]["Value"]
        print(phone_number, "this should be a phone_number")

        #converting transaction date to to datetime from string
        str_transaction_date = str(transaction_date)
        print(str_transaction_date, "this should be an str_transaction_date")

        transaction_datetime = datetime.strptime(str_transaction_date, "%Y%m%d%H%M%S")
        print(transaction_datetime, "this should be an transaction_datetime")


        our_model = LNMOnline.objects.create(
            CheckoutRequestID=checkout_request_id,
            MerchantRequestID=merchant_request_id,
            Amount=amount,
            ResultCode=result_code,
            ResultDesc=result_description,
            MpesaReceiptNumber=mpesa_receipt_number,
            Balance=balance,
            TransactionDate=transaction_datetime,
            PhoneNumber=phone_number, 
        )

        our_model.save()

        return Response({"OurResultDesc": "YEEY!!! It worked!"})

  '''  


'''
def complete(request):
    if my_access_token=='' and x=='':
        messages.info(request,'Make the transaction  first')
        return render(request,'dashboard_students/booking_confirmation.html')
    else:

        def message():
            global y
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer %s' % my_access_token
            }

            request2 = {
                "BusinessShortCode": '174379',
                "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjMxMjA3MDczNTE5",
                "Timestamp": "20231112115056",
                "CheckoutRequestID": x,
                }

            response = requests.post('https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query', headers = headers, json=request2)
            print(response.text)
            data=response.json()
            print(data)
            y=data['ResultDesc']
            print(y)
        message()
        if (y=="The service request is processed successfully."):
            
            
            new_transaction=money(amount=amount,date=date, name=request.user.get_username())
            new_transaction.save()
            messages.info(request,'Transaction complete')
            
            return render(request,'dashboard_students/booking_confirmation.html')
        else:
            messages.info(request,'You cancelled the Transaction')
            return render(request,'dashboard_students/booking_confirmation.html')
         

'''


      
