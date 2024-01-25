from rest_framework import serializers

from apps.cash_flows.models import CashFlow, CashFlowType
from apps.trades.api.serializers import TradeSerializer


class CashFlowTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlowType
        fields = '__all__'


class CashFlowSerializer(serializers.ModelSerializer):
    trade = TradeSerializer(read_only=True, source="trade_identifier")
    cash_flow_type = CashFlowTypeSerializer(read_only=True, many=True)

    class Meta:
        model = CashFlow
        fields = ["trade", "identifier", "amount", "date", "cash_flow_type"]
