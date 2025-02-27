# Generated by Django 5.1.6 on 2025-02-09 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulations', '0004_delete_expense_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('category', models.CharField(choices=[('food', 'Food'), ('transport', 'Transport'), ('utilities', 'Utilities'), ('entertainment', 'Entertainment'), ('other', 'Other')], max_length=50)),
            ],
        ),
    ]
