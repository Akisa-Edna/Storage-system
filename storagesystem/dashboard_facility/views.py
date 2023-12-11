from django.shortcuts import render,redirect
from django.views import View
#from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime,timedelta
from dashboard_students.models import Booking,Container
from django.db.models import Q
from .forms import ContainerForm
from dashboard_students.forms import BookingForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Create your views here.
'''def search_results(request):
    query = request.GET.get('query')
    results = Booking.objects.filter(booking_number__icontains=query)  # Search in the 'title' field

    return render(request, 'search_results.html', {'results': results, 'query': query})'''

def search_results(request):
    query = request.GET.get('query')
    #results = Booking.objects.filter(booking_number__icontains=query) 

    Booking_fields = ['name', 'price','rate','date_booked','email','school','start_date','end_date'] 
    Container_fields = ['name','description','price','status']

    Booking_queries = [Q(**{field + '__icontains': query}) for field in Booking_fields]
    Container_queries = [Q(**{field + '__icontains': query}) for field in Container_fields]

    Booking_q = Q()
    for q in Booking_queries:
        Booking_q |= q

    Container_q = Q()
    for q in Container_queries:
        Container_q |= q

    Booking_results = Booking.objects.filter(Booking_q)
    Container_results = Container.objects.filter(Container_q)    



    context ={
         'Booking_results': Booking_results, 
         'Container_results': Container_results,
         'query': query
    }

    return render(request, 'dashboard_facility/dashboard.html',context)
    #return render(request, 'dashboard_facility/search.html',context)

@login_required(login_url='user_login')
def Dashboard(request):
        
     # get the current date
        today = datetime.today()
        #bookings made today
        bookings = Booking.objects.filter(
            date_booked__year=today.year, date_booked__month=today.month, date_booked__day=today.day)
        paginator = Paginator(bookings, 5)    
        page_number = request.GET.get('page')
        bookings = paginator.get_page(page_number)
        
        # Total Bookings (all previous bookings)addedline
        all_bookings = Booking.objects.all()#filter(date_booked__lt=today)#lt means lessthan
        paginator = Paginator(all_bookings, 5)    
        page_number = request.GET.get('page')
        all_bookings = paginator.get_page(page_number)

        # Retrieve all containers
        containers = Container.objects.all()
        paginator = Paginator(containers, 2)    
        page_number = request.GET.get('page')
        containers = paginator.get_page(page_number)
    

      

        # loop through the orders and add the price value
        total_revenue = 0
        for booking in bookings:
            total_revenue += booking.price

        # pass total number of orders and total revenue into template
        context = {
            'bookings': bookings,
            'all_bookings': all_bookings,
            'total_revenue': total_revenue,
            'total_bookings': len(bookings),
            'containers':containers,
            'page_obj': containers,  #added during page adding
            'allpage_obj':all_bookings, #added for pagination
            'bookpage':bookings,
        }

        return render(request, 'dashboard_facility/dashboard.html', context)


@login_required(login_url='user_login')
def ViewContainer(request, pk):
    container = Container.objects.get(id=pk)
    context = {'container': container}
    return render(request, 'dashboard_facility/view_container.html', context)


@login_required(login_url='user_login')
def AddBooking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BookingForm()
    
    context = {
         'form': form
         }
    return render(request, 'dashboard_facility/add_booking.html', context)

@login_required(login_url='user_login')
def ViewBooking(request, pk):
    booking = Booking.objects.get(id=pk)
    context = {'booking': booking}
    return render(request, 'dashboard_facility/viewbooking.html', context)



@login_required(login_url='user_login')
def UpdateBooking(request,pk):
    booking=Booking.objects.get(id=pk)
    #form=BookingForm(instance=booking)
    
    if request.method == 'POST':
            form = BookingForm(request.POST,instance=booking)
            if form.is_valid():
                 form.save()
                 return redirect('dashboard')
            
    else:
        form=BookingForm(instance=booking)        
            
    context={
          'form':form,
          'booking':booking
     }
    return render(request,'dashboard_facility/update.html',context)
     

@login_required(login_url='user_login')
def DeleteBooking(request, pk):
    booking = Booking.objects.get(id=pk)
    
    booking.delete()
    return redirect('dashboard')

@login_required(login_url='user_login')
def AddContainer(request):
    if request.method == 'POST':
        form = ContainerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ContainerForm()
    
    context = {
         'form': form
         }
    return render(request, 'dashboard_facility/add_container.html', context)


@login_required(login_url='user_login')
def UpdateContainer(request,pk):
    container=Container.objects.get(id=pk)
    #form=ContainerForm(instance=container)
    
    if request.method == 'POST':
            form = ContainerForm(request.POST,instance=container)
            if form.is_valid():
                updated_container = form.save(commit=False)
            if updated_container.units > 0:
                updated_container.status = 'available'
            updated_container.save()
            return redirect('dashboard')
            '''if form.is_valid():
                 form.save()
                 return redirect('dashboard')'''
            
    else:
        form=ContainerForm(instance=container)        
            
    context={
          'form':form,
          'container':container
     }
    return render(request,'dashboard_facility/update_container.html',context)
     

@login_required(login_url='user_login')
def DeleteContainer(request, pk):
    container=Container.objects.get(id=pk)
    
    container.delete()
    return redirect('dashboard')




