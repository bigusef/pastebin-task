import string
import random


def code_generator(instance, size=7):
    chars = string.ascii_lowercase + string.digits
    code = ''.join(random.choices(chars, k=size))
    Klacc = instance.__class__
    is_exist = Klacc.objects.filter(shortcode=code).exists()
    if is_exist:
        code_generator(instance=instance, size=size)
    else:
        return code
