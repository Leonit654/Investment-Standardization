# urls.py
from django.urls import path
from .views import OrganizationListCreateView, OrganizationRetrieveUpdateDestroyView

urlpatterns = [
    path('organizations/', OrganizationListCreateView.as_view(), name='organization-list-create'),
    path('organizations/<int:pk>/', OrganizationRetrieveUpdateDestroyView.as_view(), name='organization-retrieve-update-destroy'),
]
