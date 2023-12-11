from django.contrib import admin
from django.urls import path, include

from mpesa.api.views import LNMCallbackUrlAPIView

urlpatterns = [
    path("lnm/", LNMCallbackUrlAPIView.as_view(), name="lnm-callbackurl"),
]