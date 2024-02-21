from rest_framework import generics
from .models import Organization
from .serializers import OrganizationSerializer
from rest_framework.pagination import PageNumberPagination

class NoPagination(PageNumberPagination):
    page_size = None

class OrganizationListCreateView(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    pagination_class = NoPagination  # Disable pagination

class OrganizationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
