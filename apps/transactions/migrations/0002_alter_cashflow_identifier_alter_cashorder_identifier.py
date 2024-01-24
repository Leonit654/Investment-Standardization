# Generated by Django 4.2.9 on 2024-01-24 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashflow',
            name='identifier',
            field=models.CharField(max_length=75, unique=True),
        ),
        migrations.AlterField(
            model_name='cashorder',
            name='identifier',
            field=models.CharField(max_length=75, unique=True),
        ),
    ]
