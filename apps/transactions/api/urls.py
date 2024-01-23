from django.urls import path

from apps.transactions.api.views import CashFlowView

urlpatterns = [
    path("synchronize/", CashFlowView.as_view(), name="synchronize"),
]
