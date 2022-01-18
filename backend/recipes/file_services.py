import csv
import io

import reportlab
from django.conf import settings
from django.http import FileResponse, HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

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


def create_pdf(purchases_dict):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    reportlab.rl_config.TTFSearchPath.append(
        str(settings.BASE_DIR) + '/fonts')
    pdfmetrics.registerFont(TTFont('FreeSans', '../fonts/FreeSans.ttf'))
    p.setFont('FreeSans', 16)
    p.drawString(250, 800, 'FoodGram')
    p.drawString(30, 750, 'Список покупок:')
    p.setFont('FreeSans', 14)
    x = 710
    for key, value in purchases_dict.items():
        p.drawString(30, x, f' - {key} - {value}')
        x -= 30
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=True,
        filename='Список покупок.pdf',
        content_type='application/pdf'
    )
