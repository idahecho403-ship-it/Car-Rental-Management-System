from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Customer, Booking

def index(request):
    featured_cars = Car.objects.all()[:6]
    return render(request, 'rental/index.html', {
        'featured_cars': featured_cars
    })

def update_car_statuses():
    today = date.today()

    cars = Car.objects.all()

    for car in cars:

        active_booking = Booking.objects.filter(
            car=car,
            status='Approved',
            pickup_date__lte=today,
            return_date__gte=today
        ).exists()

        if active_booking:
            if car.status != 'Booked':
                car.status = 'Booked'
                car.save(update_fields=['status'])

        else:
            # Only return the car to Available if it is not in maintenance
            if car.status == 'Booked':
                car.status = 'Available'
                car.save(update_fields=['status'])


def car_list(request):
    update_car_statuses()

    cars = Car.objects.all()

    search = request.GET.get('search', '')
    brand = request.GET.get('brand', '')
    fuel = request.GET.get('fuel', '')
    transmission = request.GET.get('transmission', '')
    status = request.GET.get('status', '')

    if search:
        cars = cars.filter(
            model__icontains=search
        ) | cars.filter(
            brand__icontains=search
        )

    if brand:
        cars = cars.filter(brand__iexact=brand)

    if fuel:
        cars = cars.filter(fuel_type__iexact=fuel)

    if transmission:
        cars = cars.filter(transmission__iexact=transmission)

    if status:
        cars = cars.filter(status__iexact=status)

    brands = Car.objects.values_list(
        'brand', flat=True
    ).distinct()

    return render(request, 'rental/car_list.html', {
        'cars': cars,
        'brands': brands,
    })



def car_detail(request, car_id):
    update_car_statuses()

    car = get_object_or_404(Car, id=car_id)

    return render(request, 'rental/car_detail.html', {
        'car': car
    })


def book_car(request, car_id):
    update_car_statuses()
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':

        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        drivers_license = request.POST.get('drivers_license', '').strip()
        pickup_date = request.POST.get('pickup_date', '')
        return_date = request.POST.get('return_date', '')

        # Check that all fields were provided
        if not all([
            full_name,
            email,
            phone,
            address,
            drivers_license,
            pickup_date,
            return_date
        ]):
            return render(request, 'rental/booking_form.html', {
                'car': car,
                'error': 'Please fill in all the required fields.'
            })

        # Check that return date is after pickup date
        if return_date <= pickup_date:
            return render(request, 'rental/booking_form.html', {
                'car': car,
                'error': 'Return date must be after the pickup date.'
            })

        # Check car availability
        if car.status != 'Available':
            return render(request, 'rental/booking_form.html', {
                'car': car,
                'error': 'Sorry, this car is currently unavailable.'
            })

        # Prevent overlapping bookings
        conflicting_booking = Booking.objects.filter(
            car=car,
            status__in=['Pending', 'Approved'],
            pickup_date__lt=return_date,
            return_date__gt=pickup_date
        ).exists()

        if conflicting_booking:
            return render(request, 'rental/booking_form.html', {
                'car': car,
                'error': 'This car is already booked for the selected dates.'
            })

        # Find existing customer or create a new one
        customer, created = Customer.objects.get_or_create(
            email=email,
            defaults={
                'full_name': full_name,
                'phone': phone,
                'address': address,
                'drivers_license': drivers_license,
            }
        )

        # Create booking
        Booking.objects.create(
            customer=customer,
            car=car,
            pickup_date=pickup_date,
            return_date=return_date,
            status='Pending'
        )

        return render(request, 'rental/booking_form.html', {
            'car': car,
            'success': 'Your booking request has been submitted successfully!'
        })

    return render(request, 'rental/booking_form.html', {
        'car': car
    })

def dashboard(request):
    today = date.today()

    # Update car statuses before showing dashboard numbers
    update_car_statuses()

    # Car statistics
    total_cars = Car.objects.count()

    available_cars = Car.objects.filter(
        status='Available'
    ).count()

    booked_cars = Car.objects.filter(
        status='Booked'
    ).count()

    # Customer statistics
    total_customers = Customer.objects.count()

    # Booking statistics
    pending_bookings = Booking.objects.filter(
        status='Pending'
    ).count()

    approved_bookings = Booking.objects.filter(
        status='Approved'
    ).count()

    returned_bookings = Booking.objects.filter(
        status='Returned'
    ).count()

    cancelled_bookings = Booking.objects.filter(
        status='Cancelled'
    ).count()

    # Currently active rentals
    active_rentals = Booking.objects.filter(
        status='Approved',
        pickup_date__lte=today,
        return_date__gte=today
    ).order_by('return_date')

    active_rentals_count = active_rentals.count()

    # Upcoming pickups
    upcoming_pickups = Booking.objects.filter(
        status='Approved',
        pickup_date__gt=today
    ).order_by('pickup_date')[:5]

    # Recent bookings
    recent_bookings = Booking.objects.order_by(
        '-id'
    )[:5]

    return render(request, 'rental/dashboard.html', {
        'total_cars': total_cars,
        'available_cars': available_cars,
        'booked_cars': booked_cars,
        'total_customers': total_customers,

        'pending_bookings': pending_bookings,
        'approved_bookings': approved_bookings,
        'returned_bookings': returned_bookings,
        'cancelled_bookings': cancelled_bookings,

        'active_rentals': active_rentals,
        'active_rentals_count': active_rentals_count,

        'upcoming_pickups': upcoming_pickups,

        'recent_bookings': recent_bookings,
    })

def about(request):
    return render(request, 'rental/about.html')


def contact(request):
    return render(request, 'rental/contact.html')