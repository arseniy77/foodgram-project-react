# Generated by Django 2.2.6 on 2022-01-13 23:49

from django.db import migrations, models
import recipes.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220110_0253'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favouriterecipe',
            options={'ordering': ['-added_to_favourite', '-added_to_shopping_cart'], 'verbose_name': 'Избранное', 'verbose_name_plural': 'Избранное'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['name', 'measurement_unit'], 'verbose_name': 'Ингридиент', 'verbose_name_plural': 'Ингридиенты'},
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(choices=[('г', 'грамм'), ('мл', 'миллилитров'), ('ст. л.', 'столовая ложка'), ('ч. л.', 'чайная ложка'), ('тушка', 'тушка'), ('шт', 'штук'), ('по вкусу', 'по вкусу'), ('стакан', 'стакан'), ('горсть', 'горсть'), ('упаковка', 'упаковка')], max_length=50, verbose_name='Единицы измерения'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(db_index=True, max_length=255, unique=True, verbose_name='Ингридиент'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(validators=[recipes.validators.CustomMinValueValidator(1)], verbose_name='Время приготовления'),
        ),
        migrations.AlterField(
            model_name='recipeingredients',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[recipes.validators.CustomMinValueValidator(1)], verbose_name='Количество ингридиента'),
        ),
    ]