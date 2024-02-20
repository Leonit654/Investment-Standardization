# Generated by Django 4.2.9 on 2024-02-20 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('identifier', models.CharField(max_length=100, unique=True)),
                ('issue_date', models.DateField(blank=True, null=True)),
                ('maturity_date', models.DateField(blank=True, null=True)),
                ('invested_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('interest_rate', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
