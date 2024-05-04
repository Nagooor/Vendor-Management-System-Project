from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from app.models import *
from app.serializers import *
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count
from django.db.models import Q
# from django.db.models import Count, F, ExpressionWrapper, DecimalField


class VendorListCreateAPIView(APIView):
    def get(self,request):
        vendors=Vendor.objects.all()
        serializer=VendorSerializer(vendors,many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer=VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'insert':'Data inserted successfull'})
        else:
            return Response({'Error':'Data insertion Error'})

class VendorRetrieveUpdateDestroyAPIView(APIView):
    def get(self,request,vendor_id):
        vendor=Vendor.objects.get(pk=vendor_id)
        serializer=VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self,request,vendor_id):
        vendor=Vendor.objects.get(pk=vendor_id)
        serializer=VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'insert':'Data inserted successfull'})
        else:
            return Response({'Error':'Data insertion Error'})

    def delete(self,request,vendor_id):
        vendor=Vendor.objects.get(pk=vendor_id)
        vendor.delete()
        return Response({'deletion':'Data is deleted'})








class PurchaseOrderListCreateAPIView(APIView):
    def get(self,request):
        vendor_id=request.query_params.get('vendor_id')
        if vendor_id:
            purchase_orders=PurchaseOrder.objects.filter(vendor_reference=vendor_id)
        else:
            purchase_orders=PurchaseOrder.objects.all()
        serializer=PurchaseOrderSerializer(purchase_orders,many=True)
        return Response({'get':'Data display successfull'})

    def post(self,request):
        serializer=PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'insert':'Data inserted successfull'})
        else:
            return Response({'Error':'Data insertion Error'})

class PurchaseOrderRetrieveUpdateDestroyAPIView(APIView):
    def get(self,request,po_id):
        purchase_order=PurchaseOrder.objects.get(pk=po_id)
        serializer=PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    def put(self,request,po_id):
        purchase_order=PurchaseOrder.objects.get(pk=po_id)
        serializer=PurchaseOrderSerializer(purchase_order,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'insert':'Data inserted successfull'})
        else:
            return Response({'Error':'Data insertion Error'})

    def delete(self,request,po_id):
        purchase_order=PurchaseOrder.objects.get(pk=po_id)
        purchase_order.delete()
        return Response({'deletion':'Data is deleted'})
    





class VendorPerformanceAPIView(APIView):
    def get(self,request,vendor_id):
        try:
            vendor=Vendor.objects.get(pk=vendor_id)
            serializer=VendorPerformanceSerializer(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response({"error":"Vendor not found"})




#Back End Logic Here........

class CalculateOnTimeDeliveryRate(APIView):
    def post(self,request):
        # Retrieve the purchase order ID from the request data
        po_id=request.data.get('po_id')
        try:
            # Retrieve the purchase order
            po=PurchaseOrder.objects.get(id=po_id)
            if po.status=='completed':
                # Retrieve the vendor
                vendor=po.vendor
                # Count the number of completed POs delivered on or before delivery_date
                completed_orders=PurchaseOrder.objects.filter(vendor=vendor,status='completed')
                on_time_orders=completed_orders.filter(delivery_date__lte=po.delivery_date)
                on_time_delivery_rate=(on_time_orders.count()/completed_orders.count())*100
                # Update vendor's On-Time Delivery Rate
                vendor.on_time_delivery_rate=on_time_delivery_rate
                vendor.save()
                return Response({'message':'On-Time Delivery Rate calculated and updated successfully.'})
            else:
                return Response({'error':'The purchase order status is not completed.'})
        except PurchaseOrder.DoesNotExist:
            return Response({'error':'Purchase order not found.'})





class UpdateQualityRatingAverage(APIView):
    def post(self,request):
        # Retrieve the purchase order ID and quality rating from the request data
        po_id=request.data.get('po_id')
        quality_rating=request.data.get('quality_rating')
        try:
            # Retrieve the purchase order
            po=PurchaseOrder.objects.get(id=po_id)
            # Ensure the purchase order is completed and quality rating is provided
            if po.status=='completed' and quality_rating is not None:
                # Retrieve the vendor
                vendor=po.vendor
                # Calculate the average of all quality_rating values for completed POs of the vendor
                completed_orders=PurchaseOrder.objects.filter(vendor=vendor,status='completed').exclude(quality_rating__isnull=True)
                total_ratings=completed_orders.aggregate(total_rating=models.Sum('quality_rating'))['total_rating']
                num_completed_orders=completed_orders.count()
                quality_rating_average=total_ratings/num_completed_orders if num_completed_orders > 0 else 0
                # Update vendor's Quality Rating Average
                vendor.quality_rating=quality_rating_average
                vendor.save()
                return Response({'message':'Quality Rating Average updated successfully.'})
            else:
                return Response({'error':'The purchase order status is not completed or quality rating is not provided.'})
        except PurchaseOrder.DoesNotExist:
            return Response({'error':'Purchase order not found.'})





class UpdateAverageResponseTime(APIView):
    def post(self,request):
        # Retrieve the purchase order ID and acknowledgment date from the request data
        po_id=request.data.get('po_id')
        acknowledgment_date_str=request.data.get('acknowledgment_date')
        try:
            # Retrieve the purchase order
            po=PurchaseOrder.objects.get(id=po_id)
            # Ensure acknowledgment date is provided
            if acknowledgment_date_str:
                acknowledgment_date=datetime.strptime(acknowledgment_date_str,'%Y-%m-%d %H:%M:%S')
                # Retrieve the vendor
                vendor=po.vendor
                # Compute the time difference between issue_date and acknowledgment_date for each PO
                time_diff=acknowledgment_date-po.issue_date
                # Update vendor's Average Response Time
                total_response_time=vendor.response_time*vendor.num_acknowledgments
                total_response_time+=time_diff.total_seconds()
                vendor.num_acknowledgments+=1
                vendor.response_time=total_response_time/vendor.num_acknowledgments
                vendor.save()
                return Response({'message':'Average Response Time updated successfully.'})
            else:
                return Response({'error':'Acknowledgment date is required.'})
        except PurchaseOrder.DoesNotExist:
            return Response({'error':'Purchase order not found.'})




class UpdateFulfilmentRate(APIView):
    def post(self,request):
        # Retrieve the purchase order ID and new status from the request data
        po_id=request.data.get('po_id')
        new_status=request.data.get('new_status')
        try:
            # Retrieve the purchase order
            po=PurchaseOrder.objects.get(id=po_id)
            # Retrieve the vendor
            vendor=po.vendor
            # Update the fulfilment rate upon any change in PO status
            if new_status=='completed':
                # Check if the PO was successfully fulfilled
                if po.issues==0:
                    vendor.successful_orders+=1
                # Increment the total number of orders issued to the vendor
                vendor.total_orders+=1
            # Calculate the fulfilment rate
            fulfilment_rate=(vendor.successful_orders/vendor.total_orders)*100 if vendor.total_orders > 0 else 0
            # Update vendor's Fulfilment Rate
            vendor.fulfilment_rate=fulfilment_rate
            vendor.save()
            return Response({'message':'Fulfilment Rate updated successfully.'})
        except PurchaseOrder.DoesNotExist:
            return Response({'error':'Purchase order not found.'})
        


# API Endpoint Implementation here....

class VendorPerformanceEndpoint(APIView):
    def get(self,request,vendor_id):
        try:
            # Retrieve the vendor
            vendor=Vendor.objects.get(pk=vendor_id)
            # Serialize vendor's performance metrics
            serializer=VendorPerformanceSerializer(vendor)
            return Response({'insert':'Data inserted successfull'})
        except Vendor.DoesNotExist:
            return Response({'error':'Vendor not found.'})

class UpdateAcknowledgmentEndpoint(APIView):
    def post(self,request,po_id):
        try:
            # Retrieve the purchase order
            po=PurchaseOrder.objects.get(pk=po_id)
            # Update acknowledgment date
            acknowledgment_date_str=request.data.get('acknowledgment_date')
            if acknowledgment_date_str:
                acknowledgment_date=datetime.strptime(acknowledgment_date_str,'%Y-%m-%d')
                po.acknowledgment_date=acknowledgment_date
                po.save()
                # Trigger recalculation of average_response_time
                po.vendor.calculate_average_response_time()
                return Response({'message':'Acknowledgment updated successfully.'})
            else:
                return Response({'error':'Acknowledgment date is required.'})
        except PurchaseOrder.DoesNotExist:
            return Response({'error':'Purchase order not found.'})
        



# Additional Technical Considerations
# Efficient Calculation:

class UpdateFulfilmentRate(APIView):
    def post(self,request):
        # Retrieve the vendor ID from the request data
        vendor_id=request.data.get('vendor_id')
        try:
            # Retrieve the vendor and calculate fulfilment rate
            vendor=Vendor.objects.annotate(
                total_orders=Count('purchaseorder'),
                successful_orders=Count('purchaseorder',filter=Q(purchaseorder__status='completed',purchaseorder__issues=0))
            ).filter(pk=vendor_id).first()
            if vendor:
                fulfilment_rate=(vendor.successful_orders*100)/vendor.total_orders if vendor.total_orders > 0 else 0
                # Update vendor's Fulfilment Rate
                vendor.fulfilment_rate=fulfilment_rate
                vendor.save()
                return Response({'message':'Fulfilment Rate updated successfully.'})
            else:
                return Response({'error':'Vendor not found.'})
        except Exception as e:
            return Response({'error':str(e)})
        

# Data Integrity:
class UpdateFulfilmentRate(APIView):
    def post(self,request):
        # Retrieve the vendor ID from the request data
        vendor_id=request.data.get('vendor_id')
        try:
            # Retrieve the vendor and calculate fulfilment rate
            vendor=Vendor.objects.annotate(
                total_orders=Count('purchaseorder'),
                successful_orders=Count('purchaseorder',filter=Q(purchaseorder__status='completed',purchaseorder__issues=0))
            ).filter(pk=vendor_id).first()
            if vendor:
                if vendor.total_orders==0:
                    fulfilment_rate=0
                else:
                    fulfilment_rate=(vendor.successful_orders*100)/vendor.total_orders
                # Update vendor's Fulfilment Rate
                vendor.fulfilment_rate=fulfilment_rate
                vendor.save()
                return Response({'message':'Fulfilment Rate updated successfully.'})
            else:
                return Response({'error':'Vendor not found.'})
        except ZeroDivisionError:
            return Response({'error':'Cannot divide by zero.'})
        except Exception as e:
            return Response({'error':str(e)})


# Real-time Updates:
@receiver(post_save,sender=PurchaseOrder)
def update_fulfilment_rate(sender, instance,**kwargs):
    if instance.status=='completed' or instance.status=='cancelled':
        # Retrieve the vendor and update fulfilment rate
        vendor=instance.vendor
        vendor.update_fulfilment_rate()
