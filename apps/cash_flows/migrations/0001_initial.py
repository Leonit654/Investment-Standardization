# Generated by Django 4.2.9 on 2024-02-20 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('trades', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashFlowType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('value', models.CharField(max_length=25)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CashFlow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('identifier', models.CharField(max_length=75, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=18)),
                ('date', models.DateField()),
                ('cash_flow_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cash_flows', to='cash_flows.cashflowtype')),
                ('trade', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cash_flows', to='trades.trade')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
