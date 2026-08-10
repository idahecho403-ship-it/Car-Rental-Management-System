from django.contrib import admin
from .models import Car, Customer, Booking
from datetime import date


# =========================
# SIMON AUTO'S ADMIN BRANDING
# =========================

admin.site.site_header = "SIMON AUTO'S MANAGEMENT"
admin.site.site_title = "Simon Auto's Admin"
admin.site.index_title = "Simon Auto's Rental Management System"


# =========================
# CAR ADMIN
# =========================

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):

    list_display = (
        'brand',
        'model',
        'year',
        'daily_price',
        'status',
        'fuel_type',
        'transmission',
    )

    list_filter = (
        'brand',
        'status',
        'fuel_type',
        'transmission',
        'year',
    )

    search_fields = (
        'brand',
        'model',
    )

    ordering = (
        'brand',
        'model',
    )

    list_per_page = 25


# =========================
# CUSTOMER ADMIN
# =========================

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        'full_name',
        'email',
        'phone',
    )

    search_fields = (
        'full_name',
        'email',
        'phone',
    )

    ordering = (
        'full_name',
    )

    list_per_page = 25


# =========================
# BOOKING ADMIN
# =========================
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        'customer',
        'car',
        'pickup_date',
        'return_date',
        'status',
    )

    list_filter = (
        'status',
        'pickup_date',
        'return_date',
    )

    search_fields = (
        'customer__full_name',
        'customer__email',
        'customer__phone',
        'car__brand',
        'car__model',
    )

    date_hierarchy = 'pickup_date'

    ordering = (
        '-pickup_date',
    )

    list_per_page = 25
def save_model(self, request, obj, form, change):

    # Save the booking first
    super().save_model(request, obj, form, change)

    today = date.today()

    # Approved booking
    if obj.status == 'Approved':

        # Only mark the car as Booked when the rental
        # has actually started
        if obj.pickup_date <= today <= obj.return_date:
            obj.car.status = 'Booked'
        else:
            obj.car.status = 'Available'

        obj.car.save(update_fields=['status'])

    # Returned or Cancelled booking
    elif obj.status in ['Returned', 'Cancelled']:

        obj.car.status = 'Available'
        obj.car.save(update_fields=['status'])