from django.core.exceptions import ValidationError


def validate_file_size(file):
    max_size_kb = 10 * 1024

    if file.size > max_size_kb * 1024:
        raise ValidationError(f'Files cannot be larger than {max_size_kb} KB!')

def validate_pdf_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', ]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Solamente son aceptados archivos PDF.')

def validate_image_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.png', '.jpg', '.jpeg' ]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Solamente son aceptados archivos en formato png y jpg.')
