from django.contrib import admin

# Register your models here.
from app.models import *

admin.site.register(Vendor)

admin.site.register(PurchaseOrder)

admin.site.register(PerformanceRecord)