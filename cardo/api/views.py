import pandas as pd
from django.forms import DecimalField
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from cardo.models import Cash_flows, Trade
from decimal import Decimal
from cardo.api.serializers import TradeSerializer, CashFlowSerializer


class UploadFileView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        cashflow_file = request.FILES.get('cash_flows')
        trade_file = request.FILES.get('trades')

        if trade_file:
            df_trades1 = pd.read_excel(trade_file)


            for index, row in df_trades1.iterrows():
                trade = Trade(
                    loan_id=row['loan_id'],
                    debtor_identifier=row['debtor_identifier'],
                    seller_identifier=row['seller_identifier'],
                    issue_date=row['issue_date'],
                    investment_date=row['investment_date'],
                    currency=row['currency'],
                    trade_receivable_amount=row['trade_receivable_amount'],
                    purchase_amount=row['purchase_amount'],
                    purchase_price=row['purchase_price'],
                    outstanding_principal_amount=row['outstanding_principal_amount'],
                    approved_limit=row['approved_limit'],
                    maturity_date=row['maturity_date'],
                    extension_date=row['extension_date'],
                    interest_rate_exp=row['interest_rate_exp'],
                    expected_net_return=row['expected_net_return'],
                    closing_date=row['closing_date'],
                    trade_receivable_status=row['trade_receivable_status'],
                    days_in_delay=row['days_in_delay'],
                    performance_status=row['performance_status'],
                    default_date=row['default_date'],
                    default_amount=row['default_amount'],
                    write_off_date=row['write_off_date'],
                    write_off_amount=row['write_off_amount'],
                    repurchased=row['repurchased'],
                    current_rating=row['current_rating'],
                    rating_source=row['rating_source'],
                    day_count_convention=row['day_count_convention'],
                    rollovered_status=row['rollovered_status'],
                    rollovered_id=row['rollovered_id'],
                    rollovered_amount=row['rollovered_amount'],
                    company_bankrupted_status=row['company_bankrupted_status'],
                    company_bankrupted_date=row['company_bankrupted_date'],
                    related_parties=row['related_parties']
                )
                trade.save()

            return Response("Trades uploaded successfully", status=200)
        elif cashflow_file:
            df_cashflows = pd.read_excel(cashflow_file)
            df_cashflows['cashflow_date'] = pd.to_datetime(df_cashflows['cashflow_date'],
                                                           format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

            for index, row in df_cashflows.iterrows():
                try:
                    trade = Trade.objects.get(loan_id=row['loan_id'])
                    amount = Decimal(row['amount'].replace(',', '').strip())
                    cashflow = Cash_flows(
                        cashflow_id=row['cashflow_id'],
                        trade=trade,
                        cashflow_date=row['cashflow_date'],
                        cashflow_currency=row['cashflow_currency'],
                        cashflow_type=row['cashflow_type'],
                        amount=amount
                    )
                    cashflow.save()
                except Trade.DoesNotExist:
                    pass
            return Response("Cash flows uploaded successfully", status=200)
        else:
            return Response("Please upload the trades file", status=400)
