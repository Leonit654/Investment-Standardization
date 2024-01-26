from rest_framework import serializers
from apps.cash_flows.models import CashFlow, Trade, CashFlowType


class CashFlowTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlowType
        fields = '__all__'


class CashFlowSerializer(serializers.ModelSerializer):
    trade_identifier = serializers.SlugRelatedField(
        slug_field='identifier',
        queryset=Trade.objects.all(),
        allow_null=True
    )
    cash_flow_type = serializers.SlugRelatedField(
        slug_field='value',
        queryset=CashFlowType.objects.all(),
    )

    class Meta:
        model = CashFlow
        fields = ["identifier", 'cash_flow_type', 'amount', 'date', "trade_identifier"]

    def create(self, validated_data):
        validated_data["trade"] = validated_data.pop("trade_identifier")

        instance = CashFlow(**validated_data)
        instance.save()
        return instance

    # def bulk_create(self, validated_data_list):
    #     cash_flows_to_create = []
    #     for validated_data in validated_data_list:
    #         validated_data["trade"] = validated_data.pop("trade_identifier")
    #         cash_flows_to_create.append(CashFlow(**validated_data))
    #
    #     CashFlow.objects.bulk_create(cash_flows_to_create)
    #     return cash_flows_to_create
