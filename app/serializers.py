from rest_framework import serializers
from app.models import *
from app.serializers import *

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields='__all__'
        # fields = ['id', 'name', 'contact_details', 'address', 'vendor_code']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=PurchaseOrder
        fields='__all__'
        # fields = ['id', 'po_number', 'vendor', 'order_date', 'items', 'quantity', 'status']


class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields='__all__'
        # fields = ['id', 'on_time_delivery_rate', 'quality_rating', 'response_time', 'fulfilment_rate']
        