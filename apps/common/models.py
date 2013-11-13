from django.db import models

# Create your models here

#Table containing the users data.
class User(models.Model):
	UserID = models.BigIntegerField(primary_key = True)
	Username = models.CharField(unique = True, max_length = 30)
	
	Email = models.EmailField(max_length=75)
	
#Table containing the existing courses and it's data
class Course(models.Model):
	CourseID = models.BigIntegerField(primary_key = True)
	CourseName = models.CharField(max_length = 260, blank = False)
	

	#CourseCode
	#CourseTerm (date)
	
	Description = models.TextField()

#Table containing relations between Users and Courses
#If a relation exists then the user can view the specified course
#This can also specify if the user can edit content
class User_Course(models.Model):
	UserID = models.ForeignKey('User')
	CourseID = models.ForeignKey('Course')
	
	PermEdits = models.BooleanField(default = False)

#Table containing existing lessons and it's data
#It also holds a relation to a course, this value cannot be null
class Lessons(models.Model):
	LessonID = models.BigIntegerField(primary_key = True)
	CourseID = models.ForeignKey('Course')
	#UserID = models.CharField(max_length = 20, blank = False)	
	
	Title = models.TextField()

#Table containing existing slides
#It also holds a relation to the lesson it is part of
class Slides(models.Model):
	SlideID = models.BigIntegerField(primary_key = True)
	Number = models.BigIntegerField()

	LessonID = models.ForeignKey('Lessons')

#Table containing the content for a slide
#Multiple content input can be created for a single slide
#
class Content(models.Model):
	ContentID = models.BigIntegetField(primary_key = True)
	Type = models.CharField(max_length = 10)
       	Data = models.TextField()
	Number = models.BigIntegerField()

	SlideID = models.ForeignKey('Slides')


#Table containing the different tags
#Need to specify if tags are selected by course, lecture or slide
#Temporarily has been set to lesson
class Subject(models.Model):
	SubjectID = models.BigIntegerField(primary_key = True)
	Type = models.CharField(max_length = 10)

	LessonID = models.ForeignKey('Lesson')

#
class Question(models.Model):
	QuestionID = models.BigIntegerField(primary_key = True)
	
	Text = models.TextField()	

	SubjectID = models.ForeignKey('Subject')
	ContentID = models.ForeignKey('Content')


#
class Answers(models.Model):
	AnswersID = models.BigIntegerField(primary_key = True)
	Correct = models.BooleanField(default = False)
	Text = models.TextField()
	
	QuestionID = model.ForeignKey('Question')
