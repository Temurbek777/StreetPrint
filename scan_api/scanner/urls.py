from django.urls import path
from .views import qr_scan_handler

urlpatterns = [
    path('api/scan/', qr_scan_handler, name='qr_scan'),
]
