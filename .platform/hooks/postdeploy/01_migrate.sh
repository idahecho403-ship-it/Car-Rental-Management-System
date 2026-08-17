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

    if python manage.py loaddata cars.json; then
        echo "Car import completed successfully."
    else
        echo "ERROR: Car import failed!"
        exit 1
    fi
else
    echo "Cars already exist or cars.json is missing. Skipping car import."
fi

echo "Final car count:"
python manage.py shell -c "from rental.models import Car; print(Car.objects.count())"