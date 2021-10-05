from airtable import Airtable
from django.shortcuts import render
from converter.config import base_key, api_key
import pdfkit
from django.template.loader import get_template
from datetime import datetime
import locale


def init(request):
    # connection with Airtable
    airtable = Airtable(base_key, 'current_course', api_key)
    # data processing
    template = get_template('diploma.html')
    for script in airtable.get_all():
        if script['fields']['course_number'][0] == 'recDHc3Fva86DKgWZ':
            if script['fields'].get('project_presented', False):
                name = script['fields']['first_name']
                surname = script['fields']['last_name']
                date = "2021-7-17"
                date = datetime.strptime(date, "%Y-%m-%d")
                locale.setlocale(locale.LC_TIME, "en_US")
                date = datetime.strftime(date, "%d %B %Y")
                html = render(request, 'diploma.html', {'name': name, 'surname': surname, 'date': date})
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
    return render(request, 'diploma.html')
