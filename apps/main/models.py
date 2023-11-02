from django.db import models
from user.models import TaxiDriver, Client
from user.tasks import task_ads


class TelegramUser(models.Model):
    telegram_id = models.CharField(unique=True, max_length=250)

    def __str__(self):
        return self.telegram_id


class Town(models.Model):
    name = models.CharField(max_length=350)

    def __str__(self):
        return self.name


class Destination(models.Model):
    taxi_driver = models.ForeignKey(TaxiDriver, models.CASCADE, related_name='destinations')
    where = models.ForeignKey(Town, models.CASCADE, related_name='destinations')
    to_where = models.ForeignKey(Town, models.CASCADE, related_name='to_destinations')

    def __str__(self):
        return self.taxi_driver.name


class Travel(models.Model):
    client = models.ForeignKey(Client, models.CASCADE, related_name='travels')
    where = models.ForeignKey(Town, models.CASCADE, related_name='travels')
    to_where = models.ForeignKey(Town, models.CASCADE, related_name='to_travels')
    lat = models.CharField(max_length=250)
    lon = models.CharField(max_length=250)
    count_person = models.CharField(max_length=250)
    note = models.TextField(null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.name} {self.completed}"


class Message(models.Model):
    travel = models.ForeignKey(Travel, models.CASCADE, related_name='messages')
    chat_id = models.CharField(max_length=221)
    message_id = models.CharField(max_length=221)

    def __str__(self):
        return self.message_id


class Advertising(models.Model):
    image = models.FileField(upload_to='advertising', null=True, blank=True)
    video = models.FileField(upload_to='advertising', null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        lst = [i.telegram_id for i in TelegramUser.objects.all()]
        image = None
        video = None
        if self.image:
            image = self.image.path
        elif self.video:
            video = self.video.path
        super().save()
        task_ads.delay(image=image, video=video, text=self.text, lst=lst)
