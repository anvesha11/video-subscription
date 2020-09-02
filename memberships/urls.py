from django.urls import path
from .views import MembershipSelectView, PaymentView, updateTransactionRecords, profile_view, cancelSubscription

app_name = 'memberships'

urlpatterns = [
    #we don't wanna have a path to admin here so put an empty string
    #remember to add forward slash at the end of path, won't work otherwise
    path('', MembershipSelectView.as_view(), name='select'),
    path('payment/', PaymentView, name='payment'),
    path('update-transactions/<subscription_id>/', updateTransactionRecords, name='update-transactions'),
    path('profile/', profile_view, name='profile'),
    path('cancel/', cancelSubscription, name='cancel'),
]

#remember to put the app url into project urls