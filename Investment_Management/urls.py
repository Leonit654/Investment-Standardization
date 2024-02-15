
from django.contrib import admin
from django.urls import path, include
# from apps.trades.api.views import TradesWithCashflowView
from apps.common.views import Synchronizer, TaskDetails, GetColumns, ConfigurationCreateView, ConfigurationByOrgIdView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("trades/", include("apps.trades.api.urls")),
    # path("synchronize/", TradesWithCashflowView.as_view(), name="synchronize"),
    path("cash_flows/", include("apps.cash_flows.api.urls")),
    path("synchronize", Synchronizer.as_view()),
    path('task/<str:task_id>/', TaskDetails.as_view(), name='task-details'),
    path('columns', GetColumns.as_view(), name='get-columns'),
    path('save-configuration', ConfigurationCreateView.as_view(), name='configuration-create'),
    path('get-configs/<int:org_id>/', ConfigurationByOrgIdView.as_view(), name='configuration-get'),
    path('org/', include('apps.organization.urls'), name='organization')

]
