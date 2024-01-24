import json

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from apps.trades.models import Trade
from services.synchronizer import Synchronizer


class TradeMappingView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        file = request.FILES.get('file')
        column_mapping = json.loads(request.data.get('column_mapping', None))
        synchronizer = Synchronizer(file, file_type="trade", columns_to_rename=column_mapping)
        df = synchronizer.run()

        # Trade.create(df.to_dict(orient="records"))
        return Response("Trades uploaded successfully", status=200)
