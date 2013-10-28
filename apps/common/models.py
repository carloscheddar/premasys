from django.db import models

# Create your models here

class User(models.Model):
	UserID = models.BigIntegerField(primary_key = True)
	Username = models.CharField(max_length = 30)
	email = models.EmailField(max_length=75)
	perm = models.BooleanField(default = False)
	
class Course(models.Model):
	CourseName = models.CharField(max_length = 260, blank = False)
	CourseID = models.BigIntegerField(primary_key = True)
	
class User_Course(models.Model):
	Prof_CourID = models.BigIntegerField(primary_key = True)
	UserID = models.ForeignKey('User')
	CourseID = models.ForeignKey('Course')

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
	
