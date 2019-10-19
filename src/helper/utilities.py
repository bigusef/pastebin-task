import csv
import string
import random
from django.http import HttpResponse


def code_generator(instance: object, size=7) -> str:
    """
    genrate unique code based on snippet.Pastes model
    if generated code is exisit this function with ren again to genrate another code
    :return string unique code
    """
    chars = string.ascii_lowercase + string.digits
    code = ''.join(random.choices(chars, k=size))
    Klacc = instance.__class__
    is_exist = Klacc.objects.filter(shortcode=code).exists()
    if is_exist:
        code_generator(instance=instance, size=size)
    else:
        return code


def csv_file_render(headers: list, context: list):
    """
    CSV helper function this function responsibe on return genrated CSV file from data passed to function
    :parameters
    headers is list and contain all file headers
    context is list of objects and include all file data
    :return HTTP respons hold file to download
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csv_render.csv"'
    writer = csv.DictWriter(response, fieldnames=headers)
    writer.writeheader()
    writer.writerows(context)
    return response
