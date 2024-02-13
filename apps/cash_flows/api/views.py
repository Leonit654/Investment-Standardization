from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.serializers import InputSerializer
from services.synchronizer import Synchronizer


class CashFlowView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        serializer = InputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        values_to_replace = serializer.validated_data.get(
            "values_to_replace", {}
        )
        merge_columns = serializer.validated_data.get(
            "merge_columns", {}
        )
        synchronizer = Synchronizer(
            serializer.validated_data["file"],
            file_type="cash_flow",
            columns_to_rename=serializer.validated_data["column_mapping"],
            merge_columns=merge_columns,
            values_to_replace=values_to_replace,
        )
        synchronizer.run()

        return Response("Cash flows uploaded successfully", status=200)
