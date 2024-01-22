from datetime import datetime
from decimal import Decimal
from django.core.files.storage import FileSystemStorage
from django.db import models



class Trade(models.Model):
    identifier = models.CharField(max_length=100, primary_key=True)
    debtor_identifier = models.CharField(max_length=50, blank=True)
    seller_identifier = models.CharField(max_length=50, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    invested_amount = models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)
    maturity_date = models.DateField(null=True, blank=True)
    interest_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def daily_interest_rate(self):
        interest_rate = self.interest_rate
        daily_interest_rate_percent = interest_rate / 100
        daily_interest_rate = daily_interest_rate_percent / 365

        return daily_interest_rate

    def daily_interest_amount(self):
        funding_cashflows = self.cashflows.filter(operation__transaction_type='funding')
        print(funding_cashflows)
        invested_amount_value = 0
        for funding_cashflow in funding_cashflows:
            invested_amount_value -= funding_cashflow.amount
        invested_amount = abs(invested_amount_value)
        daily_interest_rate = Decimal(self.daily_interest_rate())
        return invested_amount * daily_interest_rate

    def passed_days(self, reference_date):
        reference_date_value = datetime.strptime(reference_date, "%Y-%m-%d").date()
        return (reference_date_value - self.issue_date).days

    def gross_expected_interest_amount(self, reference_date):

        return self.daily_interest_amount() * self.passed_days(reference_date)

    def gross_expected_amount(self, reference_date):
        funding = self.cashflows.filter(operation__transaction_type='funding')
        invested_amount_value = 0
        for i in funding:
            invested_amount_value -= i.amount
        invested_amount = abs(invested_amount_value)

        return invested_amount + self.gross_expected_interest_amount(reference_date)

    def realized_amount(self, reference_date):
        reference_date = datetime.strptime(reference_date, "%Y-%m-%d")
        repayment_values = self.cashflows.filter(operation__transaction_type__icontains='repayment',
                                                 timestamp__lte=reference_date)
        realized_amount = sum([cashflow.amount for cashflow in repayment_values])
        return realized_amount

    def remaining_invested_amount(self, reference_date):
        funding = self.cashflows.filter(operation__transaction_type='funding')
        invested_amount_value = 0
        for i in funding:
            invested_amount_value -= i.amount
        invested_amount = abs(invested_amount_value)
        return invested_amount - self.realized_amount(reference_date)

    class Meta:
        verbose_name_plural = "Trades"

    def __str__(self):
        return f"Trade: {self.identifier}"


class Cash_flows(models.Model):
    platform_transaction_id = models.CharField(primary_key=True, max_length=75)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, db_column='trade_identifier', related_name="cashflows")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateField()
    operation = models.ForeignKey(to="Operators", related_name="operations", on_delete=models.CASCADE)


class Operators(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_type = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.transaction_type}"


fs = FileSystemStorage(location="./uploads/")


class RawData(models.Model):
    file_id = models.IntegerField(primary_key=True)
    file_title = models.CharField(max_length=255)
    file = models.FileField(storage=fs)
