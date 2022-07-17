
import locale
from datetime import date, datetime

from django.shortcuts import render
from django.conf import settings
import pdfkit
from pyairtable import Table
from pyairtable.formulas import match


def init(request):
    # connection with Airtable
    formula = match({"course_number": "25 набор", "project_presented": 1})
    table = Table(settings.AIRTABLE_API_KEY, settings.AIRTABLE_BASE_ID, 'current_course')
    # data processing
    for script in table.all(formula=formula):
        name = script['fields']['first_name']
        surname = script['fields']['last_name']
        cert_date = date(2022, 4, 16)
        locale.setlocale(locale.LC_TIME, "ru_RU")
        cert_date = datetime.strftime(cert_date, "%d %B %Y")
        html = render(request, 'diploma_ru.html', {'name': name, 'surname': surname, 'date': cert_date})
        result = (html.content).decode('utf-8')
        config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
        options = {
            'dpi': 300,
            'page-size': 'A4',
            'orientation': 'landscape',
            'margin-top': '0',
            'margin-right': '0.',
            'margin-bottom': '0.',
            'margin-left': '0',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'no-outline': None
        }
        pdfkit.from_string(result, 'result/' + '{}-{}.pdf'.format(name, surname), configuration=config, options=options)
    return render(request, 'diploma_ru.html')
