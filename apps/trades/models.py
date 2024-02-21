from datetime import datetime

from django.db import models
from django.db.models import Sum
from decimal import Decimal
from apps.common.models import TimeStamp
from apps.organization.models import Organization


class Trade(TimeStamp):
    identifier = models.CharField(max_length=100, unique=True)
    issue_date = models.DateField(null=True, blank=True)
    maturity_date = models.DateField(null=True, blank=True)
    invested_amount = models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True)
    interest_rate = models.FloatField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='trades')
    def get_realized_amount(self, reference_date):
        try:
            repayments = self.cash_flows.filter(
                date__lt=reference_date,
                cash_flow_type__value__in=["principal_repayment", "interest_repayment", "general_repayment"]
            )

            return repayments.aggregate(Sum("amount"))["amount__sum"] or 0
        except Exception as e:
            print(f"Error in get_realized_amount: {str(e)}")
            return 0

    def get_gross_expected_amount(self, reference_date_str):
        try:
            reference_date = datetime.strptime(reference_date_str, "%Y-%m-%d").date()
            invested_amount = abs(
                self.cash_flows.filter(cash_flow_type__value="funding").aggregate(
                    Sum("amount")
                )["amount__sum"]
                or 0
            )
            daily_interest_rate = self.interest_rate
            daily_interest_amount = invested_amount * Decimal(str(daily_interest_rate))
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
                self.cash_flows.filter(cash_flow_type__value="funding").aggregate(
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
            cash_flows_list = list(self.cash_flows.all())
            for cashflow in cash_flows_list:
                gross_expected_amount = self.get_gross_expected_amount(str(self.maturity_date))
                if cashflow.cash_flow_type.value in ["principal_repayment", "interest_repayment", "general_repayment"]:
                    realized_amount = self.get_realized_amount(cashflow.date)
                    if realized_amount >= gross_expected_amount:
                        return "Loan Closed!"

            return "Loan Not Closed!"

        except Exception as e:
            raise Exception(f"Error in get_closing_date: {str(e)}")

