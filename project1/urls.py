"""
URL configuration for project1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/vendors/', VendorListCreateAPIView.as_view()),
    path('api/vendors/<int:vendor_id>/', VendorRetrieveUpdateDestroyAPIView.as_view()),

    path('api/purchase_orders/', PurchaseOrderListCreateAPIView.as_view()),
    path('api/purchase_orders/<int:po_id>/', PurchaseOrderRetrieveUpdateDestroyAPIView.as_view()),

    path('api/vendors/<int:vendor_id>/performance/', VendorPerformanceAPIView.as_view()),

    # Backend logic class based views here...
    path('api/calculate_on_time_delivery_rate/', CalculateOnTimeDeliveryRate.as_view()),

    path('api/update_quality_rating_average/', UpdateQualityRatingAverage.as_view()),

    path('api/update_average_response_time/', UpdateAverageResponseTime.as_view()),

    path('api/update_fulfilment_rate/', UpdateFulfilmentRate.as_view()),

    # API Endpoint Implementation here....
    path('api/vendors/<int:vendor_id>/performance/', VendorPerformanceEndpoint.as_view()),
    path('api/purchase_orders/<int:po_id>/acknowledge/', UpdateAcknowledgmentEndpoint.as_view()),

    # Vendor Performance Endpoint
    path('api/vendors/<int:vendor_id>/performance/', VendorPerformanceEndpoint.as_view()),
    # Update Acknowledgment Endpoint
    path('api/purchase_orders/<int:po_id>/acknowledge/', UpdateAcknowledgmentEndpoint.as_view()),
    # Update Fulfilment Rate Endpoint
    path('api/vendors/<int:vendor_id>/update_fulfilment_rate/', UpdateFulfilmentRate.as_view()),

 ]
