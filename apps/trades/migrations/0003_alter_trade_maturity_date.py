# Generated by Django 4.2.9 on 2024-01-25 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trades", "0002_alter_trade_interest_rate_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trade",
            name="maturity_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
