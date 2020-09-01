from django.urls import path
from .views import MembershipSelectView, PaymentView, updateTransactions

app_name = 'memberships'

urlpatterns = [
    #we don't wanna have a path to admin here so put an empty string
    #remember to add forward slash at the end of path, won't work otherwise
    path('', MembershipSelectView.as_view(), name='select'),
    path('payment/', PaymentView, name='payment'),
    path('update-transactions/<subscription_id>/', updateTransactions, name='update-transaction')
]

#remember to put the app url into project urls