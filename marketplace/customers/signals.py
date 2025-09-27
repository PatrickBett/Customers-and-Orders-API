#post_save - a signal that fires after a model is saved
from django.db.models.signals import post_save
# receiver → decorator that allows us to register a function as a signal handler
from django.dispatch import receiver
# Import the Order model (so we can listen for changes on it)
from .models import Order
# Import our custom SMS sending utility function
from utils.sms import send_sms

@receiver(post_save, sender=Order)
def send_order_sms(sender, instance, created, **kwargs):
    if created:
        customer = instance.customer
        message = f"Hello {customer.name}, your order for {instance.item} of amount {instance.amount} has been received."
        send_sms(customer.phone_number, message)