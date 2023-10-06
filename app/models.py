from django.db import models

class scrapeData(models.Model):
    URL = models.URLField(max_length=200)
    Name_Of_Img = models.CharField(max_length=200)
    Date_Time = models.DateTimeField(auto_now_add=True)
