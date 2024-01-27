import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from apps.common.serializers import InputSerializer
from apps.trades.api.serializers import TradeSerializer
from apps.trades.models import Trade
from services.synchronizer import Synchronizer


class TradeMappingView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        serializer = InputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        synchronizer = Synchronizer(serializer.validated_data['file'],

                                    file_type="trade",

                                    columns_to_rename=serializer.validated_data["column_mapping"],
                                    )
        try:
            synchronizer.run()
        except Exception as e:
            raise e
        return Response("Trades uploaded successfully", status=200)


class TradesWithCashflowView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        serializer = InputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        synchronizer = Synchronizer(serializer.validated_data['file'],

                                    columns_to_rename=serializer.validated_data["column_mapping"],
                                    multiple_sheets=serializer.validated_data["sheet_mapping"],
                                    values_to_replace=serializer.validated_data["values_to_replace"]
                                    )
        try:
            synchronizer.run()
        except Exception as e:
            raise e
        return Response("Trades and chash flows  uploaded successfully", status=200)
