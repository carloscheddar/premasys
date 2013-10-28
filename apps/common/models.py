from django.db import models

# Create your models here

class User(models.Model):
	UserID = models.BigIntegerField(primary_key = True)
	Username = models.CharField(max_length = 30)
	
	Email = models.EmailField(max_length=75)
	
class Course(models.Model):
	CourseName = models.CharField(max_length = 260, blank = False)
	CourseID = models.BigIntegerField(primary_key = True)
	
	Description = models.TextField()
	
class User_Course(models.Model):
	UserID = models.ForeignKey('User')
	CourseID = models.ForeignKey('Course')
	
	PermEdits = models.BooleanField(default = False)

class Lessons(models.Model):
	LessonID = models.BigIntegerField(primary_key = True)
	CourseID = models.ForeignKey('Course')
	#UserID = models.CharField(max_length = 20, blank = False)	
	
	Title = models.TextField()

class Slides(models.Model):
	SlideID = models.BigIntegerField(primary_key = True)
	Number = models.BigIntegerField()
	Data = models.TextField()
	LessonID = models.ForeignKey('Lessons')
