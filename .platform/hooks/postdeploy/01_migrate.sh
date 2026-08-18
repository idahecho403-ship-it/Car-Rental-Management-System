#!/bin/bash

cd /var/app/current
source /var/app/venv/*/bin/activate

echo "========================================"
echo "SIMON AUTOS DEPLOYMENT"
echo "========================================"

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Checking car database..."

CAR_COUNT=$(python manage.py shell -c "from rental.models import Car; print(Car.objects.count())" | tail -n 1)

echo "Current car count: $CAR_COUNT"

if [ "$CAR_COUNT" = "0" ] && [ -f /var/app/current/cars.json ]; then
    echo "AWS database has no cars. Importing cars.json..."

    python manage.py loaddata /var/app/current/cars.json

    echo "Car import completed."
else
    echo "Cars already exist or cars.json is missing. Skipping car import."
fi

echo "========================================"
echo "FIXING SQLITE PERMISSIONS"
echo "========================================"

APP_USER=$(/opt/elasticbeanstalk/bin/get-config platformconfig -k AppUser)

echo "Elastic Beanstalk application user: $APP_USER"

echo "Fixing application directory..."

chown "$APP_USER:$APP_USER" /var/app/current
chmod 775 /var/app/current

if [ -f /var/app/current/db.sqlite3 ]; then

    echo "SQLite database found."

    chown "$APP_USER:$APP_USER" /var/app/current/db.sqlite3
    chmod 664 /var/app/current/db.sqlite3

fi

echo "Fixing SQLite temporary files if they exist..."

for file in /var/app/current/db.sqlite3-*; do
    if [ -e "$file" ]; then
        chown "$APP_USER:$APP_USER" "$file"
        chmod 664 "$file"
    fi
done

echo "SQLite directory permissions:"
ls -ld /var/app/current

echo "SQLite database permissions:"
ls -la /var/app/current/db.sqlite3*

echo "========================================"
echo "TESTING DATABASE WRITE"
echo "========================================"

python manage.py shell <<'PYTHON'

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("CREATE TABLE IF NOT EXISTS _sqlite_write_test (id INTEGER PRIMARY KEY)")
    cursor.execute("DROP TABLE _sqlite_write_test")

print("DATABASE WRITE TEST: SUCCESS")

PYTHON

echo "========================================"
echo "FINAL CAR COUNT"
echo "========================================"

python manage.py shell -c "from rental.models import Car; print('FINAL CAR COUNT:', Car.objects.count())"

echo "========================================"
echo "DEPLOYMENT COMPLETE"
echo "========================================"