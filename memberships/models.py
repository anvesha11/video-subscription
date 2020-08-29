from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

from datetime import datetime
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


MEMBERSHIP_CHOICES = (
    ('Enterprise', 'ent'),
    ('Professional', 'pro'),
    ('Free', 'free')
)


class Membership(models.Model):
    slug = models.SlugField()
    membership_type = models.CharField(
        choices=MEMBERSHIP_CHOICES,
        default='Free',
        max_length=30)
    price = models.IntegerField(default=15)
    stripe_plan_id = models.CharField(max_length=40)

    def __str__(self):
        return self.membership_type


class UserMembership(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=40)
    membership = models.ForeignKey(
        Membership, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

# post save is the signal which creates user memberships
# hence we have imported it

#as we have created a post save receiver we need to delete the database
#and make migrations again
def post_save_usermembership_create(sender, instance, created, *args, **kwargs):
    if created:
        UserMembership.objects.get_or_create(user=instance)

    user_membership, created = UserMembership.objects.get_or_create(
        user=instance)

    #this means there is no stripe customer id currently
    if user_membership.stripe_customer_id is None or user_membership.stripe_customer_id == '':
        #makes a customer on the stripe backend, all we need to do is pass the email
        #this returns an object and we are grabbing the id field from that
        #for user_membership_stripe_customer_id
        new_customer_id = stripe.Customer.create(email=instance.email)
        
        free_membership = Membership.objects.get(membership_type='Free')
        user_membership.stripe_customer_id = new_customer_id['id']
        user_membership.membership = free_membership
        user_membership.save()


post_save.connect(post_save_usermembership_create,
                  sender=settings.AUTH_USER_MODEL)


class Subscription(models.Model):
    user_membership = models.ForeignKey(
        UserMembership, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=40)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.user.username
