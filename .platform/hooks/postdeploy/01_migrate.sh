#!/bin/bash

cd /var/app/current

source /var/app/venv/*/bin/activate

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Checking car database..."

CAR_COUNT=$(python manage.py shell -c "from rental.models import Car; print(Car.objects.count())" | tail -n 1)

echo "Current car count: $CAR_COUNT"

if [ "$CAR_COUNT" = "0" ] && [ -f cars.json ]; then
    echo "AWS database has no cars. Importing cars.json..."
    python manage.py loaddata cars.json
    echo "Car import completed."
else
    echo "Cars already exist or cars.json is missing. Skipping car import."
fi