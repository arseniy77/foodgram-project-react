from django.core.validators import MinValueValidator


class CustomMinValueValidator(MinValueValidator):
    message = 'Введенное значение не должно быть нулём!'
