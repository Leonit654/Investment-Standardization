from rest_framework import serializers
from apps.trades.models import Trade
from apps.cash_flows.models import CashFlow, CashFlowType


# TODO: remove this line if it is not needed

class CustomSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            # Try to get the Trade object from the database using the provided value
            trade_obj = Trade.objects.get(identifier=data)
            return trade_obj
        except Trade.DoesNotExist:
            # If the Trade object is not found, return None
            return None


class CashFlowTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlowType
        fields = ['id', 'value']


class CashFlowSerializer(serializers.ModelSerializer):
    trade_identifier = CustomSlugRelatedField(
        queryset=Trade.objects.all(), allow_null=True, required=False,
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
