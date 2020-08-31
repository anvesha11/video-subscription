from django.shortcuts import render

from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import ListView
from django.urls import reverse
from .models import Membership, UserMembership 

def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None

def get_user_subscription(request):
    user_subscription_qs = Subcription.objects.filter(
        user_membership=get_user_membership(request))
    if user_subscription_qs.exists():
        user_subscription = user_subscription_qs.first()
        return user_subscription
    return None

#it's called select View because it now only shows the user the membership types to choose from
#but also let's select you and begin your new membership from form provision
class MembershipSelectView(ListView):
    model = Membership
    
    #this is a build-in method which grabs the context
    def get_context_data(self, *args, **kwargs):
        #this context grabs all the variables which are being displayed by this model
        context = super().get_context_data(**kwargs)

        #here when we call the get_user_membership method, it goes there and grabs the details and name of the current membership the user has
        current_membership = get_user_membership(self.request) #as it's a class based view, use self.request, only request won't work
        #current_membership is actually a string so type cast that to string for it to actually work
        context['current_membership'] = str(current_membership.membership) #we need to grab the membership object using .membership
        return context

    #now let's handle the post request when the user actually selects a new membership and goes to subscribe it
    def post(self, request, **kwargs):
        #parsing the name of the input that you'd like to get the value of (here it's membership_type)
        #what we're getting in selected_membership is the value of the input, ent or pro
        selected_membership = request.POST.get('membership_type')
        
        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)

        #checking whether the selected membership is same as user's current membership
        selected_membership_qs = Membership.objects.filter(
            membership_type=selected_membership #selected_membership is coming from the post
        )
        if selected_membership_qs.exists():
            selected_membership = selected_membership_qs.first()
            #now we have the selected membership object and not just the string

        '''
        ====================
        VALIDATION
        ====================
        '''

        if user_membership == selected_membership:
            if user_subscription !=None:
                messages.info(request, "You already have this membership. Your next \
                payment is due {}".format('get this value from stripe'))

                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        #now we pass the selected membership into the lesson or the next view this is done by using sessions
        #assign to the session
        request.sessio['selected_membership_type'] = selected_membership.membership_type

        return HttpResponseRedirect(reverse('memberships:payment'))