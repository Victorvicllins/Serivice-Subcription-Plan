from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse
from .models import Membership, UserMembership, Subscription

# Create your views here.
def get_user_membership(request):
	user_membership_qs = UserMembership.objects.filter(user=request.user)
	if user_membership_qs.exists():
		return user_membership_qs.first()
	return None

def get_user_subscription(request):
	user_subscription_qs = Subscription.objects.filter(user_membership=get_user_membership(request))
	if user_subscription_qs.exists():
		user_subscription = user_subscription_qs.first()
		return user_subscription
	return None

def get_selected_membership(request):
	membership_type = request.session['selected_membership_type']
	selected_membership_qs = Membership.objects.filter(membership_type=membership_type)
	if selected_membership_qs.exists():
		return selected_membership_qs.first()
	return None

class MembershipSelectView(ListView):
	model = Membership
	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		current_membership = get_user_membership(self.request)
		context['current_membership'] = str(current_membership.membership)

		return context
	def post(self, request, **kwargs):
		selected_membership_type = request.POST.get('membership_type')
		price = request.POST.get('price')
		user_membership = get_user_membership(request)
		user_subscription = get_user_subscription(request)

		selected_membership_qs = Membership.objects.filter(membership_type=selected_membership_type)
		if selected_membership_qs.exists():
			selected_membership = selected_membership_qs.first()

		'''
		==========
		==========
		'''
		if user_membership.membership == selected_membership:
			if user_subscription != None:
				messages.info(request, "You already have this membership. Subscription is valid till {}".format('get Subscription expiry date.'))
				return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

		request.session['selected_membership_type'] = selected_membership.membership_type
		return HttpResponseRedirect(reverse('memberships:payment'))

def paymentView(request):
	user_membership = get_user_membership(request)
	selected_membership = get_selected_membership(request)
	# Remember to pass all Vogue requirements into session

	context = {
		'selected_membership': selected_membership,
	}
	return render(request, "memberships/memberships_payment.html", context)
