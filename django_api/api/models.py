from django.db import models
from django.utils import timezone

class LivePost(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    title = models.CharField(max_length=255)
    body = models.TextField()
    waktu_penarikan = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'transactions_manual_trigger'  # Ini akan menjadi nama tabel baru Anda di pgAdmin

