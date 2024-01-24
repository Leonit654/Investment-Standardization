import json

from pandas.core.methods.to_dict import to_dict
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
        Trade.create(data=df.to_dict(orient="records"))
        return Response("Trades uploaded successfully", status=200)