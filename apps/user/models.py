from django.db import models


class TaxiDriver(models.Model):
    telegram_id = models.CharField(max_length=250)
    username = models.CharField(max_length=250, null=True)
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    telegram_id = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    username = models.CharField(max_length=250, null=True)
    phone = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def travels_count(self):
        return self.travels.count()


class Payment(models.Model):
    taxi_driver = models.ForeignKey(TaxiDriver, models.CASCADE, related_name='payments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.taxi_driver.name
