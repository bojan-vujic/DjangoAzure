from django.db import models

class File(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    file_name    = models.CharField(max_length=200, null=True)
    file = models.FileField(default='default.png', upload_to='myfiles', blank=True, null=True)
    