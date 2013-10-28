from django.shortcuts import render_to_response
from django.template import RequestContext
from reveal.models import Lesson

from common.models import User
from common.models import Course
from common.models import User_Course
from common.models import Lesson
from common.models import Slides


def Reveal(request):
	return render_to_response("index.html", RequestContext(request, {'title': 'Test Reveal'} ) )

def Edit(request):
  return render_to_response("edit.html", RequestContext(request, {'title': 'Edit'}))




###----------------------------###
#
# Calls to the common models
#
# returns data pulled
###----------------------------###

def Save_Lesson(lesson):
	ID = lesson["ID"]
	Lesson(LessionId = ID).save()
	for slide in lesson["slides"]:
		Slides(LessonID = ID, Number = slide["num"], Data = slide["data"]).save()


	return lesson
#

def Get_Slides(L_ID):
	slides=[]

	return slides
	
