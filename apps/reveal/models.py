from django.db import models

class Lesson(models.Model):
	username = models.CharField(max_length=50)
	slide = models.TextField()
