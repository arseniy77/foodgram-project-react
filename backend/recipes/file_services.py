import csv

from django.conf import settings
from django.http import HttpResponse

from .models import Ingredient


def import_csv():
    with open(settings.INGREDIENTS_CSV_FILENAME) as csvfile:
        reader = csv.DictReader(
            csvfile, fieldnames=('name', 'measurement_unit')
        )
        for row in reader:
            name = row['name']
            measurement_unit = row['measurement_unit']
            Ingredient.objects.get_or_create(
                name=name,
                measurement_unit=measurement_unit
            )

        return HttpResponse('Ok')
