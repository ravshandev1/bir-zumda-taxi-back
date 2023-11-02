from .models import Payment
from datetime import datetime, timedelta


def subscribe(user):
    obj = Payment.objects.filter(user=user).last()
    if (datetime.now() - obj.created_at) > timedelta(days=30):
        return False
    return True
