import paystack
import uuid
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
# Create your models here.
paystack.api_key = settings.PAYSTACK_SECRET_KEY

def autoKey():
	sample = uuid.uuid4()
	key = hex(int(sample.time_low))
	return key

MEMBERSHIP_CHOICES = (
		('Enterprise', 'Ent'),
		('Professional', 'Pro'),
		('Free', 'Free'),
	)
class Membership(models.Model):
	slug = models.SlugField()
	membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES, default='Free')
	price = models.IntegerField(default=15)
	paystack_plan_id = models.CharField(max_length=50, default=autoKey())

	def __str__(self):
		return self.membership_type

class PaystackPayment(models.Model):
	customer = models.CharField(max_length=100)
	user_key = models.CharField(max_length=200, default=autoKey())
	amount	 = models.DecimalField(max_digits=10, decimal_places=2, null=True)

	def __str__(self):
		return self.customer

class UserMembership(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	paystack_customer_id = models.CharField(max_length=50)
	membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True)
	def __str__(self):
		return self.user.name

def post_save_usermembership_create(sender, instance, created, *args, **kwargs):
	if created:
		UserMembership.objects.get_or_create(user=instance)
	user_membership, created = UserMembership.objects.get_or_create(user=instance)
	if user_membership.paystack_customer_id is None or user_membership.paystack_customer_id == '':
		new_customer_id = PaystackPayment.objects.create(customer=instance.email)
		user_membership.paystack_customer_id = new_customer_id.user_key
		user_membership.save()

post_save.connect(post_save_usermembership_create, sender=settings.AUTH_USER_MODEL)

class Subscription(models.Model):
	user_membership = models.ForeignKey(UserMembership, on_delete=models.CASCADE)
	paystack_subscription_id = models.CharField(max_length=50)
	active = models.BooleanField(default=True)
	def __str__(self):
		return self.user_membership.user.name

