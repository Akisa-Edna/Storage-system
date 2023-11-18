from django.shortcuts import render,redirect
from django.contrib import messages
from . models import*
from datetime import datetime
import logging
from .forms import BookingForm
from .constants import PICKUP_PRICE, LORRY_PRICE,SUBCOUNTIES_AND_RATES,schools_list
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse



# Create your views here.
   
@login_required(login_url='user_login')
def Container_booking(request):
   shared_space = Container.objects.filter(category__name__contains='shared_spaces')
   private_space = Container.objects.filter(category__name__contains='private_spaces')

   context = {
       'shared_spaces': shared_space,
       'private_spaces': private_space,
    }
   
   return render(request,'dashboard_students/book_cont.html',context)

def Booked_cont(request):
      pass


@login_required(login_url='user_login')
def Book_spaces(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user  # Get the authenticated user
            if hasattr(user, 'student'):
                #student = request.user.student
                name = request.POST.get('name')
                email = request.POST.get('email')
                phonenumber = request.POST.get('phonenumber')
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')
                #county = request.POST.get('county')
                #subcounty = request.POST.get('subcounty')
                
                

                price = 0
                space_ids = []

                booking_spaces = {'spaces': []}

                # Get the selected space IDs from the form
                spaces = request.POST.getlist('spaces[]')
                print(spaces)

                if start_date and end_date:
                    try:
                        start_date_obj = datetime.fromisoformat(start_date)
                        end_date_obj = datetime.fromisoformat(end_date)
                    except ValueError:
                        messages.error(request, "Invalid date format.")
                        return render(request, 'dashboard_students/cont_book.html')

                    if start_date_obj > end_date_obj:
                        messages.error(request, "End date should be after start date.")
                        return render(request, 'dashboard_students/cont_book.html')

                for space_id in spaces:
                    try:
                      container = Container.objects.get(pk=int(space_id))

                        # Container has available units, proceed with the booking
                      if container.units > 0:
                            # Calculate the number of days
                            start_date_obj = datetime.fromisoformat(start_date)
                            end_date_obj = datetime.fromisoformat(end_date)
                            num_days = (end_date_obj - start_date_obj).days + 1  # Add 1 to include the end date

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

                              space_data = {
                                 'id': container.pk,
                                 'name': container.name,
                                 'price': individual_price #or container.price
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
                        # Handle the case where a selected space does not exist
                        pass

                if len(space_ids) > 0:  # Create the booking record only if there are selected spaces
                    # Create the booking record
                    booking = Booking.objects.create(
                        price=sum(space['price'] for space in booking_spaces['spaces']),
                        #price=price,
                        name=name,
                        email=email,
                        phonenumber=phonenumber,
                        start_date=start_date,
                        end_date=end_date,
                        student=user.student  # Associate the booking with the student
                    )

                    booking.spaces.add(*space_ids)

                    context = {
                        'booking':booking,
                        'spaces': booking_spaces['spaces'],
                        'price': price,
                        'booking_id': booking.id  # Include the booking ID for reference
                    }

                    return render(request, 'dashboard_students/booking_confirmation.html', context)
                    #return render(request, 'dashboard_students/book_cont.html', context)
                    #return render(request, 'dashboard_students/booking_confirmation.html', context)

                else:
                    # Handle the case where no spaces were selected for booking
                    messages.error(request, "No spaces were selected for booking.")

    # If the request method is not POST or the user is not authenticated, render the form
    return render(request, 'dashboard_students/book_cont.html')




def index(request):
    subcounties_and_rates = {
        'Subcounty1': {'pickup': 10, 'lorry': 20},
        'Subcounty2': {'pickup': 15, 'lorry': 25},
        'Subcounty3': {'pickup': 12, 'lorry': 22},
        # Add more subcounties and rates as needed
    }

    if request.method == 'POST':
        selected_subcounty = request.POST.get('subcounty')
        if selected_subcounty:
            rates = subcounties_and_rates.get(selected_subcounty, {})
            return render(request, 'view_rates.html', {'subcounty': selected_subcounty, 'rates': rates})

    subcounties = list(subcounties_and_rates.keys())
    return render(request, 'index.html', {'subcounties': subcounties})


'''@login_required(login_url='user_login')
def Book_spaces(request):
    if request.user.is_authenticated :
      if request.method == 'POST':
        user = request.user  # Get the authenticated user
        if hasattr(user, 'student'):
            #student = request.user.student
            name = request.POST.get('name')
            email = request.POST.get('email')
            phonenumber = request.POST.get('phonenumber')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            #county = request.POST.get('county')
            #subcounty = request.POST.get('subcounty')
            #school = request.POST.get('school')

            price = 0
            space_ids = []

            booking_spaces = {
                'spaces': []
            }
            # Get the selected space IDs from the form
            spaces = request.POST.getlist('spaces[]')

            if start_date and end_date:   
                try:
                 start_date_obj = datetime.fromisoformat(start_date)
                 end_date_obj = datetime.fromisoformat(end_date)
                except ValueError:
                 messages.error(request, "Invalid date format.")
                 return render(request, 'dashboard_students/cont_book.html')

                if start_date_obj > end_date_obj:
                  messages.error(request, "End date should be after start date.")
                  return render(request, 'dashboard_students/cont_book.html')


            for space_id in spaces:
                try:
                    container = Container.objects.get(pk=int(space_id))

                    # Container has available units, proceed with the booking
                    if container.units > 0:
                          # Calculate the number of days
                      start_date_obj = datetime.fromisoformat(start_date)
                      end_date_obj = datetime.fromisoformat(end_date)
                      num_days = (end_date_obj - start_date_obj).days + 1  # Add 1 to include the end date

                      # Use the monthly rate as the space price
                      space_price = container.price  # Assuming container.price represents the monthly rate

                      # Calculate the price based on the number of days
                      if num_days in [30, 31]:
                        price = space_price
                      else:
                      # Assuming there are 30 or 31 days in a month for simplicity
                        daily_rate = space_price / 30  # Calculate daily rate based on monthly rate
                        cont_price = num_days * daily_rate

                    
                        space_data = {
                          'id': container.pk,
                          'name': container.name,
                          #'price': container.price
                          'price':cont_price or container.price
                         }
                        booking_spaces['spaces'].append(space_data)

                        #units  available code
                        # Decrease the number of units and update status
                        container.units -= 1
                        container.update_status()

                        price += cont_price or container.price
                        # price += container.price
                        space_ids.append(container.pk)

                    else :
                        # Container has 0 units, prevent booking
                        messages.error(request, f"container.name} is fully booked and unavailable.") 

                except Container.DoesNotExist:
                    # Handle the case where a selected space does not exist
                    pass
                
            if len(space_ids) > 0: # Create the booking record only if there are selected spaces
                    
                  # Create the booking record
                booking = Booking.objects.create(
                price=price,
                name=name,
                email=email,
                phonenumber=phonenumber,
                start_date=start_date,
                end_date=end_date,
                #county=county,
                #subcounty=subcounty,
                #school=school,
                student=user.student  # Associate the booking with the student
                )

                booking.spaces.add(*space_ids)

                context = {
                'spaces': booking_spaces['spaces'],
                'price': price,
                'booking_id': booking.id  # Include the booking ID for reference
                }
                  #return redirect('booking_confirmation.html')
                return render( request,'dashboard_students/booking_confirmation.html',context)
            
            else:
                 # Handle the case where no spaces were selected for booking
                 messages.error(request, "No spaces were selected for booking.")
                
    # If the request method is not POST or the user is not authenticated, render the form
    return render(request, 'dashboard_students/cont_book.html')  '''

'''def date_range_view(request):
  if request.user.is_authenticated :
    if request.method == 'POST':
        user = request.user 
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Create and save a booking instance
            booking = Booking.objects.create(
                start_date=start_date,
                end_date=end_date,
                student=user.student
                # Add other fields as needed
            )
            context ={
                'form':form,
                'booking':booking
            }

            # Redirect to a confirmation page or wherever you want
            return redirect('booking_confirmation')  
    else:
        form = DateRangeForm()

    return render(request, 'dashboard_students/cont_book.html', context)  '''



def ViewContainer(request, pk):
    container = Container.objects.get(id=pk)
    context = {'container': container}
    return render(request, 'dashboard_students/viewcontainer.html', context)




def Collect(request,booking_id):
    booking = Booking.objects.get(pk=booking_id)
    
    subcounties = list(SUBCOUNTIES_AND_RATES.keys())  # Move this outside the if block
    print(subcounties)

    #previous_price = booking.price 
    if request.method == 'POST':
         
        selected_subcounty = request.POST.get('subcounty')
        if selected_subcounty:
            rates = SUBCOUNTIES_AND_RATES.get(selected_subcounty, {})

            #  selected_rate = request.POST.get('rate', 0)  # Assuming 'rate' is the name of the form field
            #   total_price = previous_price + float(selected_rate)

            #    booking.price = total_price
            #   booking.save()

            context = {
                'subcounty': selected_subcounty, 
                'rates': rates,
             #        'total_price':total_price,
                'booking_id':booking_id,
                'booking':booking
            }


            return render(request, 'dashboard_students/viewrates.html', context)

    return render(request, 'dashboard_students/luggage_collection.html', {'subcounties': subcounties},{'booking':booking}) 


'''def get_rates(request):
    subcounties = list(SUBCOUNTIES_AND_RATES.keys())  # Move this outside the if block
    if request.method == 'POST' :
        selected_subcounty = request.POST.get('subcounty')
        if selected_subcounty:
          rates = SUBCOUNTIES_AND_RATES.get(selected_subcounty, {})
        return JsonResponse(rates)
    #return JsonResponse({}, status=400)
    booking = None  # If booking is relevant here, retrieve it based on your logic
    schools = None  # Define your schools_list based on your requirements
    context = {
        'subcounties': subcounties,
        'booking': booking,
        'schools_list': schools,
    }
    return render(request, 'dashboard_students/luggage_collection.html', context)'''

         




@login_required(login_url='user_login')
def LuggageCollection(request, booking_id):
    # Get the booking based on the booking_id
    try:
        booking = Booking.objects.get(pk=booking_id)
        schools = schools_list
        subcounties = list(SUBCOUNTIES_AND_RATES.keys())  # Move this outside the if block
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
                #selected_rate = request.POST.get('rate')
                selected_rate = request.POST.get('selected_rate') 

             #if rates:
               # selected_rate = request.POST.get('selected_rate')  # Assuming this is a hidden field in your form

            if selected_school and selected_subcounty:
               booking.subcounty = selected_subcounty
               booking.school = selected_school
             #booking.subcounty=selected_subcounty
            booking.rate=(selected_rate)
             # booking.school=selected_school

            if selected_rate is not None:
                previous_price = booking.price if booking.price else Decimal('0')
                total_price = previous_price + Decimal(selected_rate)
                booking.price = total_price
            #total_price=previous_price + Decimal(selected_rate)
           # booking.price += total_price
 

            booking.save() 
                
            context = {
                'rates':rates,
                'subcounty':selected_subcounty,
                'rate':selected_rate,
                #'total_price':total_price,
                'booking':booking
                }
               
            return render(request, 'dashboard_students/viewrates.html',context)
        
        ''' booking.subcounty=selected_subcounty
            booking.save()
               # booking.selected_vehicle = selected_subcounty
             #booking.rate = selected_rate
            #booking.subcounty = selected_subcounty
            #booking.save()
            
            context = {
                'subcounty': selected_subcounty, 
               # 'rates': rates,
                'booking':booking,
                'school':school,
                'schools_list': schools,
                
            }
            return render(request, 'dashboard_students/viewrates.html', context)'''
            
        
    except Booking.DoesNotExist:
        pass
    return render(request, 'dashboard_students/luggage_collection.html', {'subcounties': subcounties,'booking':booking,'schools_list':schools})     



def ConfirmRates(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    # Additional logic or data retrieval for the confirm_rates page

    return render(request, 'dashboard_students/confirm_rates.html', {'booking': booking})


'''if request.method == 'POST':
        # Handle the form submission with the transportation choice
        transportation_choice = request.POST.get('transportation_choice')

        # Process the choice and calculate the price, update the booking, etc.
        if transportation_choice == 'pickup':
                collection_price =Decimal (PICKUP_PRICE)
        else: 
          transportation_choice == 'lorry'
          collection_price = Decimal(LORRY_PRICE)

        # Calculate the total price, including the base price and transportation cost
        total_price = booking.price + collection_price

        # Update the booking with the transportation choice and the new total price
        booking.transportation_choice = transportation_choice
        booking.price = total_price
        booking.save()

        context = {
        'booking': booking,
        }


        # Redirect to a confirmation page or any other appropriate action.
        return render(request, 'dashboard_students/collectluggage_confirmation.html', context)

    
return render(request, 'dashboard_students/luggage_collection.html') '''


'''
def Collect(request):
    subcounties = list(SUBCOUNTIES_AND_RATES.keys())
        print(subcounties)

    if request.method == 'POST':
        selected_subcounty = request.POST.get('subcounty')
        if selected_subcounty:
            rates = SUBCOUNTIES_AND_RATES.get(selected_subcounty, {})
            return render(request, 'view_rates.html', {'subcounty': selected_subcounty, 'rates': rates})

       
    return render(request, 'dashboard_students/luggage_collection.html', {'subcounties': subcounties})'''

def Collect(request,id):
  
    
    booking = Booking.objects.get_or_404(pk=id)
    

    subcounties = list(SUBCOUNTIES_AND_RATES.keys())  # Move this outside the if block
    print(subcounties)

    if request.method == 'POST':
        selected_subcounty = request.POST.get('subcounty')
        if selected_subcounty:
            rates = SUBCOUNTIES_AND_RATES.get(selected_subcounty, {})

            return render(request, 'dashboard_students/viewrates.html', {'subcounty': selected_subcounty, 'rates': rates},{'booking':booking})


    return render(request, 'dashboard_students/luggage_collection.html', {'subcounties':subcounties},{'booking':booking}) 


'''def Collect(request):
    subcounties = list(SUBCOUNTIES_AND_RATES.keys())

    if request.method == 'POST':
        selected_subcounty = request.POST.get('subcounty')
        if selected_subcounty:
            rates = SUBCOUNTIES_AND_RATES.get(selected_subcounty, {})

       # selected_rate = request.POST.get('selected_rate')

        if selected_subcounty:
            # Save the data to the database
            booking = Booking(subcounty=selected_subcounty,) #rate=selected_rate)
            booking.save()

            # For demonstration purposes, let's print the selected subcounty and rate.
            print(f"Selected Subcounty: {selected_subcounty} ")

            rates = SUBCOUNTIES_AND_RATES.get(selected_subcounty, {})
            return render(request, 'dashboard_students/viewrates.html', {'subcounty': selected_subcounty, 'rates': rates })

    return render(request, 'dashboard_students/luggage_collection.html', {'subcounties': subcounties})'''




