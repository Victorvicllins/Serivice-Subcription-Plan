from django.contrib import admin
from .models import Membership, PaystackPayment, UserMembership, Subscription
# Register your models here.

admin.site.register(Membership)
admin.site.register(PaystackPayment)
admin.site.register(UserMembership)
admin.site.register(Subscription)
