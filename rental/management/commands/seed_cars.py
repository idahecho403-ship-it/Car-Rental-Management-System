from django.core.management.base import BaseCommand
from rental.models import Car


class Command(BaseCommand):
    help = "Seed luxury cars"

    def handle(self, *args, **kwargs):

        if Car.objects.exists():
            self.stdout.write(self.style.WARNING("Cars already exist."))
            return

        cars = [

            {
                "brand": "Lamborghini",
                "model": "Huracán EVO",
                "year": 2023,
                "color": "Yellow",
                "seats": 2,
                "transmission": "Automatic",
                "fuel_type": "Petrol",
                "daily_price": 1200,
                "status": "Available",
                "description": "High-performance Italian supercar.",
                "image": "https://images.unsplash.com/photo-1544636331-e26879cd4d9"
            },

            {
                "brand": "Lamborghini",
                "model": "Aventador SVJ",
                "year": 2022,
                "color": "Green",
                "seats": 2,
                "transmission": "Automatic",
                "fuel_type": "Petrol",
                "daily_price": 2500,
                "status": "Available",
                "description": "Flagship V12 Lamborghini.",
                "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70"
            },

            {
                "brand": "Ferrari",
                "model": "SF90 Stradale",
                "year": 2024,
                "color": "Red",
                "seats": 2,
                "transmission": "Automatic",
                "fuel_type": "Hybrid",
                "daily_price": 2600,
                "status": "Available",
                "description": "Hybrid Ferrari hypercar.",
                "image": "https://images.unsplash.com/photo-1553440569-bcc63803a83d"
            },

            {
                "brand": "Ferrari",
                "model": "Roma",
                "year": 2023,
                "color": "Silver",
                "seats": 2,
                "transmission": "Automatic",
                "fuel_type": "Petrol",
                "daily_price": 1700,
                "status": "Available",
                "description": "Elegant grand tourer.",
                "image": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7"
            },

            {
                "brand": "Rolls-Royce",
                "model": "Phantom",
                "year": 2024,
                "color": "Black",
                "seats": 5,
                "transmission": "Automatic",
                "fuel_type": "Petrol",
                "daily_price": 2300,
                "status": "Available",
                "description": "Ultimate luxury sedan.",
                "image": "https://images.unsplash.com/photo-1502877338535-766e1452684a"
            },

            {
                "brand": "Rolls-Royce",
                "model": "Cullinan",
                "year": 2024,
                "color": "White",
                "seats": 5,
                "transmission": "Automatic",
                "fuel_type": "Petrol",
                "daily_price": 2400,
                "status": "Available",
                "description": "Luxury SUV.",
                "image": "https://images.unsplash.com/photo-1511919884226-fd3cad34687c"
            },

            {
                "brand": "Bentley",
                "model": "Continental GT",
                "year": 2023,
                "color": "Blue",
                "seats": 4,
                "transmission": "Automatic",
                "fuel_type": "Petrol",
                "daily_price": 1600,
                "status": "Available",
                "description": "Luxury grand tourer.",
                "image": "https://images.unsplash.com/photo-1503736334956-4c8f8e92946d"
            },

            {
                "brand": "McLaren",
                "model": "720S",
                "year": 2023,
                "color": "Orange",
                "seats": 2,
                "transmission": "Automatic",
                "fuel_type": "Petrol",
                "daily_price": 2200,
                "status": "Available",
                "description": "British supercar.",
                "image": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341"
            },

            {
                "brand": "Porsche",
                "model": "911 Turbo S",
                "year": 2024,
                "color": "Grey",
                "seats": 4,
                "transmission": "Automatic",
                "fuel_type": "Petrol",
                "daily_price": 1400,
                "status": "Available",
                "description": "Iconic German sports car.",
                "image": "https://images.unsplash.com/photo-1502161254066-6c74afbf07aa"
            },

            {
                "brand": "Mercedes-Benz",
                "model": "G63 AMG",
                "year": 2024,
                "color": "Black",
                "seats": 5,
                "transmission": "Automatic",
                "fuel_type": "Petrol",
                "daily_price": 1200,
                "status": "Available",
                "description": "Luxury performance SUV.",
                "image": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d"
            }

        ]

        for car in cars:
            Car.objects.create(**car)

        self.stdout.write(
            self.style.SUCCESS(f"{len(cars)} luxury cars added successfully!")
        )