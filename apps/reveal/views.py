from django.shortcuts import render_to_response
from django.template import RequestContext
from reveal.models import Lesson

from common.models import User
from common.models import Course
from common.models import User_Course
from common.models import Lessons
from common.models import Slides


def Reveal(request):
	return render_to_response("index.html", RequestContext(request, {'title': 'Test Reveal'} ) )

def Edit(request):
  return render_to_response("edit.html", RequestContext(request, {'title': 'Edit'}))

<<<<<<< HEAD



###----------------------------###
#
# Calls to the common models
#
# returns data pulled
###----------------------------###

def Save_Lesson(lesson):
	ID = lesson["LessonID"]
	#Lesson(LessionId = ID).save()
	for slide in lesson["Slides"]:
		Slides(LessonID = ID, Number = slide["Number"], Data = slide["Data"]).save()


	return lesson
#

def Get_Slides(L_ID):
	return sorted(Slides.objects.all().filter(LessonID = L_ID), key =lambda item: item['Number'])

def Get_Lesson(L_ID):
	lesson = Lesson.objects.filter(LessonID = L_ID)
	lesson["Slides"] = Get_Slides(L_ID)

	return lesson
	
=======
def Save(request):
	post = request.POST.keys()[0]
	Lesson(username=request.user, slide=post).save()
	return render_to_response("save.html", RequestContext(request,{'h': 'hello'}))
>>>>>>> 18d1f9d7e5f5b37ddeda8ca1849a4651fe8556d5
