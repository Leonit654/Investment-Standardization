from rest_framework import serializers
from apps.trades.models import Trade


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ['identifier', 'issue_date', 'maturity_date', 'invested_amount', 'interest_rate']

    def update(self, instance, validated_data):
        # Update the existing instance with the validated data
        instance.identifier = validated_data.get('identifier', instance.identifier)
        instance.issue_date = validated_data.get('issue_date', instance.issue_date)
        instance.maturity_date = validated_data.get('maturity_date', instance.maturity_date)
        instance.invested_amount = validated_data.get('invested_amount', instance.invested_amount)
        instance.interest_rate = validated_data.get('interest_rate', instance.interest_rate)
        instance.save()
        return instance

    def create(self, validated_data):
        # TODO: handle errors regarding trade not found and object already exists
        validated_data["identifier"] = validated_data.pop("identifier")

        instance = Trade(**validated_data)
        instance.save()
        return instance
