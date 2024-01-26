from django.urls import path
from apps.trades.api.views import *

urlpatterns = [
    path("synchronize/", TradeMappingView.as_view(), name="synchronize"),

]

