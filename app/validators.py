import os
from django.core.exceptions import ValidationError


def validate_file(value):
    
    ext = os.path.splitext(value.name)[1]  
    valid_extensions = ['.pdf']
    #размер файла хранится в байтах, тут ограничений на 10 мб и формат pdf
    if not ext.lower() in valid_extensions or value.size > 1000000:
        raise ValidationError(u'Unsupported file extension.')