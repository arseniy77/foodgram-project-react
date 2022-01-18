from django.core.validators import MinValueValidator


class CustomMinValueValidator(MinValueValidator):
    message = 'Введенное значение времени должно быть больше нуля!'
