# Generated by Django 2.1 on 2020-07-31 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='stripe_subsription_id',
            new_name='stripe_subscription_id',
        ),
    ]
