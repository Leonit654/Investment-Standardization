from datetime import datetime

from django.db import models
from django.db.models import Sum


class Trade(models.Model):
    identifier = models.CharField(max_length=100, primary_key=True)
    debtor_identifier = models.CharField(max_length=50, blank=True)
    seller_identifier = models.CharField(max_length=50, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    invested_amount = models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)
    maturity_date = models.DateField(null=True, blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    class Meta:
        verbose_name_plural = "Trades"

    def __str__(self):
        return f"Trade: {self.identifier}"

    def get_realized_amount(self, reference_date):
        try:
            repayments = self.cashflows.filter(
                timestamp__lte=reference_date,
                operation__transaction_type__in=["principal_repayment", "interest_repayment", "general_repayment"]
            )

            return repayments.aggregate(Sum("amount"))["amount__sum"] or 0
        except Exception as e:
            print(f"Error in get_realized_amount: {str(e)}")
            return 0

    def get_gross_expected_amount(self, reference_date_str):
        try:
            reference_date = datetime.strptime(reference_date_str, "%Y-%m-%d").date()
            invested_amount = abs(
                self.cashflows.filter(operation__transaction_type="funding").aggregate(
                    Sum("amount")
                )["amount__sum"]
                or 0
            )
            daily_interest_rate = self.interest_rate / 365
            daily_interest_amount = invested_amount * daily_interest_rate
            passed_days = (reference_date - self.issue_date).days
            gross_expected_interest_amount = daily_interest_amount * passed_days
            gross_expected_amount = invested_amount + gross_expected_interest_amount
            return gross_expected_amount

        except Exception as e:
            print(f"Error in get_gross_expected_amount: {str(e)}")
            return 0

    def get_remaining_invested_amount(self, reference_date):
        try:
            invested_amount = abs(
                self.cashflows.filter(operation__transaction_type="funding").aggregate(
                    Sum("amount")
                )["amount__sum"]
                or 0
            )
            return invested_amount - self.get_realized_amount(reference_date)
        except Exception as e:
            print(f"Error in get_remaining_invested_amount: {str(e)}")
            return 0

    def get_closing_date(self):
        try:
            # ... (unchanged)

            cash_flows_list = list(self.cashflows.all())
            for cashflow in cash_flows_list:
                gross_expected_amount = self.get_gross_expected_amount(str(self.maturity_date))
                if cashflow.operation.transaction_type == "repayment":
                    realized_amount = self.get_realized_amount(cashflow.timestamp)
                    if realized_amount >= gross_expected_amount:
                        return f"{cashflow.timestamp} with the last repayment amount of {cashflow.amount} {cashflow.operation.transaction_type}"

            return "Loan Not Closed!"

        except Exception as e:
            raise Exception(f"Error in get_closing_date: {str(e)}")

class Cash_flows(models.Model):
    platform_transaction_id = models.CharField(primary_key=True, max_length=75)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, db_column='trade_identifier', related_name="cashflows")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateField()
    operation = models.ForeignKey(to="Operators", related_name="operations", on_delete=models.CASCADE)

class Operators(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_type = models.CharField(max_length=25)




class RawData(models.Model):
    # Fields for your model
    title = models.CharField(max_length=255)
    description = models.TextField()

    # FileField to store a file
    file = models.FileField(upload_to='raw-data-file/')