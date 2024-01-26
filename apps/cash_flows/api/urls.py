from django.urls import path

from apps.cash_flows.api.views import CashFlowView

urlpatterns = [
    path("synchronize/", CashFlowView.as_view(), name="synchronize"),

]
