from django.db import models

# Create your models here.
class Buttons(models.Model): #Added this whole class
  button_text = models.CharField(max_length=255)
  audio_text = models.CharField(max_length=255)
  user_id = models.IntegerField()
