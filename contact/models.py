from django.db import models

# Create your models here.
class QuestionAndAnswer(models.Model):
	title = models.TextField()
	body = models.TextField()

