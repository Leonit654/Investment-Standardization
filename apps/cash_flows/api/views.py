from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.cash_flows.api.serializers import CashFlowSerializer, CashFlowTypeSerializer
from apps.cash_flows.models import CashFlow, CashFlowType


class CashFlowView(APIView):
    def get(self, request, format=None):
        cash_flows = CashFlow.objects.all()
        serializer = CashFlowSerializer(cash_flows, many=True)
        return Response(serializer.data)


class CashFlowDetailView(APIView):
    def get(self, request, identifier):
        cash_flow = CashFlow.objects.get(identifier=identifier)
        serializer = CashFlowSerializer(cash_flow)
        return Response(serializer.data)

    def put(self, request, identifier):
        cash_flow = CashFlow.objects.get(identifier=identifier)
        serializer = CashFlowSerializer(cash_flow, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, identifier):
        cash_flow = CashFlow.objects.get(identifier=identifier)
        cash_flow.delete()
        return Response(f"Cash Flow with identifier {identifier} deleted", status=status.HTTP_204_NO_CONTENT)


class CashFlowTypeView(APIView):
    def get(self, request):
        cash_flow_types = CashFlowType.objects.all()
        serializer = CashFlowTypeSerializer(cash_flow_types, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CashFlowTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CashFlowTypeDetailsView(APIView):
    def get(self, request, value):
        cash_flow_type = CashFlowType.objects.get(value=value)
        serializer = CashFlowTypeSerializer(cash_flow_type)
        return Response(serializer.data)

    def put(self, request, value):
        cash_flow_type = CashFlowType.objects.get(value=value)
        serializer = CashFlowTypeSerializer(cash_flow_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, value):
        cash_flow_type = CashFlowType.objects.get(value=value)
        cash_flow_type.delete()
        return Response(f"Cash Flow with value: {value} deleted", status=status.HTTP_204_NO_CONTENT)
