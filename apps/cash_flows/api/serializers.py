from rest_framework import serializers
from apps.trades.models import Trade
from apps.cash_flows.models import CashFlow, CashFlowType


class CashFlowTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlowType
        fields = ['id', 'value']


class CashFlowSerializer(serializers.ModelSerializer):
    trade_identifier = serializers.SlugRelatedField(
        read_only=True,
        slug_field='identifier'
    )
    cash_flow_type = serializers.SlugRelatedField(
        slug_field='value',
        queryset=CashFlowType.objects.all(),
    )

    class Meta:
        model = CashFlow
        fields = ["identifier", "trade_identifier", "amount", "date", "cash_flow_type"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.trade is not None:
            representation['trade_identifier'] = instance.trade.identifier
        else:
            representation['trade_identifier'] = None

        return representation
