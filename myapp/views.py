from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking, Service, Customer
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

def home(request):
    return render(request, 'home.html')

def services(request):
    return render(request, 'services.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def show_booking_form(request, service_id):
    services = {
        1: {"name": "Light", "description": "Een basisreiniging voor uw voertuig.", "price": "€99,99"},
        2: {"name": "Light Plus", "description": "Uitgebreide basisreiniging.", "price": "€119,99"},
        3: {"name": "Light Premium", "description": "Basisreiniging met extra's.", "price": "€139,99"},
        4: {"name": "Standard", "description": "Standaard pakket met extra voordelen.", "price": "€149,99"},
    }
    service = services.get(service_id)
    if not service:
        return render(request, '404.html')
    return render(request, 'book.html', {'service': service})

def book_appointment(request):
    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        messages.success(request, 'Uw reservering werd bevestigd. Gelieve uw mailbox te controleren.')
        send_mail(
            subject='Bevestiging van uw Carwash Reservering',
            message=(
                f'Beste {first_name} {last_name},\n\n'
                f'Bedankt voor uw reservering bij Carwash Detailing.\n\n'
                f'Overzicht van uw reservering:\n'
                f'Service: {service_name}\n'
                f'Datum: {appointment_date}\n'
                f'Uur: {appointment_time}\n'
                f'Telefoonnummer: {phone_number}\n\n'
                'We kijken ernaar uit u te verwelkomen. Mocht u vragen hebben, neem dan gerust contact met ons op.\n\n'
                'Met vriendelijke groet,\nCarwash Detailing'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return redirect('home')
    else:
        return redirect('show_booking_form')

def admin_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_staff)(view_func))
    return decorated_view_func

@admin_required
def admin_dashboard(request):
    context = {
        'total_bookings': Booking.objects.count(),
        'total_services': Service.objects.count(),
        'total_customers': Customer.objects.count(),
    }
    return render(request, 'admin/dashboard.html', context)

@admin_required
def manage_bookings(request):
    bookings = Booking.objects.all()
    return render(request, 'admin/manage_bookings.html', {'bookings': bookings})

@admin_required
def manage_services(request):
    services = Service.objects.all()
    return render(request, 'admin/manage_services.html', {'services': services})

@admin_required
def manage_customers(request):
    customers = Customer.objects.all()
    return render(request, 'admin/manage_customers.html', {'customers': customers})

@admin_required
def edit_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    return redirect('manage_bookings')

@admin_required
def delete_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    booking.delete()
    return redirect('manage_bookings')

@admin_required
def edit_service(request, id):
    service = get_object_or_404(Service, id=id)
    if request.method == 'POST':
        service.name = request.POST.get('name')
        service.description = request.POST.get('description')
        service.price = request.POST.get('price')
        service.save()
        return redirect('manage_services')
    return render(request, 'admin/edit_service.html', {'service': service})

@admin_required
def delete_service(request, id):
    service = get_object_or_404(Service, id=id)
    service.delete()
    return redirect('manage_services')

@admin_required
def edit_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    if request.method == 'POST':
        customer.first_name = request.POST.get('first_name')
        customer.last_name = request.POST.get('last_name')
        customer.email = request.POST.get('email')
        customer.phone_number = request.POST.get('phone_number')
        customer.save()
        return redirect('manage_customers')
    return render(request, 'admin/edit_customer.html', {'customer': customer})

@admin_required
def delete_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    customer.delete()
    return redirect('manage_customers')

def admin_dashboard(request):
    services = Service.objects.all()
    customers = Customer.objects.all()
    bookings = Booking.objects.all()
    context = {
        'services': services,
        'customers': customers,
        'bookings': bookings,
    }
    return render(request, 'admin/dashboard.html', context)
