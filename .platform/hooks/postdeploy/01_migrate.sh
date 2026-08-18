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

echo "Checking admin account..."

python manage.py shell <<'PYTHON'
from django.contrib.auth import get_user_model

User = get_user_model()

username = "lilvix999"
email = "idahecho403@gmail.com"
password = "carrental"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print("Admin account created successfully.")
else:
    print("Admin account already exists. No changes made.")
PYTHON

echo "Final car count:"
python manage.py shell -c "from rental.models import Car; print(Car.objects.count())"