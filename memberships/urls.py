from django.urls import path
from .views import MembershipSelectView

app_name = 'memberships'

urlpatterns = [
    #we don't wanna have a path to admin here so put an empty string
    path('', MembershipSelectView.as_view(), name='select'),
]

#remember to put the app url into project urls