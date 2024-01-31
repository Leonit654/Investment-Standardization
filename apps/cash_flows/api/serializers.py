from rest_framework import serializers
from apps.trades.models import Trade
from apps.cash_flows.models import CashFlow, CashFlowType

# TODO: remove this line if it is not needed


class CashFlowTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlowType
        fields = ['id', 'value']


class CashFlowSerializer(serializers.ModelSerializer):
    trade_identifier = serializers.SlugRelatedField(queryset=Trade.objects.all(), allow_null=True, required=False,
                                                    slug_field='identifier')
    cash_flow_type = serializers.SlugRelatedField(
        slug_field='value',
        queryset=CashFlowType.objects.all(),
    )

    class Meta:
        model = CashFlow
        fields = ["identifier", "trade_identifier", "amount", "date", "cash_flow_type"]

    def create(self, validated_data):
        # TODO: handle errors regarding trade not found and object already exists
        validated_data["trade"] = validated_data.pop("trade_identifier")

        instance = CashFlow(**validated_data)
        instance.save()
        return instance