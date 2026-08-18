from django.db import models

class ApiPost(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    title = models.CharField(max_length=255)
    body = models.TextField()
    waktu_penarikan = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False 
        db_table = 'transactions'