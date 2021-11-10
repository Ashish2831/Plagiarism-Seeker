from django.db import models

# Create your models here.
class Question(models.Model):
    question = models.CharField(max_length=5000)
    image = models.FileField(upload_to='QuestionsImages/', blank=True, null=True)
    