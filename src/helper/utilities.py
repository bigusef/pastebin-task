import csv
import string
import random
from django.http import HttpResponse


def code_generator(instance, size=7):
    chars = string.ascii_lowercase + string.digits
    code = ''.join(random.choices(chars, k=size))
    Klacc = instance.__class__
    is_exist = Klacc.objects.filter(shortcode=code).exists()
    if is_exist:
        code_generator(instance=instance, size=size)
    else:
        return code


def csv_file_render(headers: list, context: list):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csv_render.csv"'
    writer = csv.DictWriter(response, fieldnames=headers)
    writer.writeheader()
    writer.writerows(context)
    return response
