from django.db import models

# Create your models here



class Course(models.Model):
	CourseName = models.CharField(max_length = 260, blank = False)
	CourseID = models.BigIntegerField(primary_key = True)


class Lessons(models.Model):
	LessonID = models.BigIntegerField(primary_key = True)
	CourseID = models.ForeignKey('Course')
	UserID = models.CharField(max_length = 20, blank = False)	

class Slides(models.Model):
	SlideID = models.BigIntegerField()
	Number = models.BigIntegerField()
	Data = models.TextField()
	LessonID = models.ForeignKey('Lessons')
	
