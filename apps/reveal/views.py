from django.shortcuts import render_to_response
from django.template import RequestContext
from reveal.models import Lesson

from common.models import User
from common.models import Course
from common.models import User_Course
from common.models import Lessons
from common.models import Slides
from common.models import Content


def Reveal(request):
	return render_to_response("index.html", RequestContext(request, {'title': 'Test Reveal'} ) )

def Edit(request):
  return render_to_response("edit.html", RequestContext(request, {'title': 'Edit'}))

def Save(request):
	post = request.POST.keys()[0]
	Lesson(username=request.user, slide=post).save()
	return render_to_response("save.html", RequestContext(request,{'h': 'hello'}))


###----------------------------###
#
# Calls to the common models
#
# returns data pulled
###----------------------------###

#SUMBIT LESSON TO DB

def Save_Lesson(lesson):
	ID = lesson["LessonID"]
	#Lesson(LessionId = ID).save()
	for slide in lesson["Slides"]:
		Slides(LessonID = ID, Number = slide["Number"]).save()
		
		for content in slide["Content"]:
			Content(SlideID=slide["SlideID"], Type = content["Type"], Data = content["Data"]).save()

	return lesson


#FIND LESSON AND SLIDES FUNCTIONS

def Get_Slides(L_ID):
	return sorted(Slides.objects.all().filter(LessonID = L_ID), key =lambda item: item['Number'])
#Revisar para usar Content() model para conseguir la info
#slide["Content"] = Content.Objects.all().filter(SlideID = slide["SlideID"]


def Get_Lesson(L_ID):
	lesson = Lesson.objects.filter(LessonID = L_ID)
	lesson["Slides"] = Get_Slides(L_ID)

	return lesson

	
### VIEW A COURSE OR LESSON FUNCTIONS

def Permit_View(C_ID, U_ID):
	Check_Course = User_Course.objects.filter(CourseID = C_ID, UserID = U_ID)
	if():#check if relation user to course exists
		return (True, Check_Course["PermEdits"]) #If it does exist return the True and the permit value
	else:#there is no relation
		return (False, False)

def Permit_Edit(C_ID, U_ID):
	Check_Course = User_Course.objects.filter(CourseID = C_ID, UserID = U_ID)
	if(): #check if relation user to course exists
		return Check_Course["PermEdits"]) #If it does exist return the permit value
	else: #there is no relation
		return False
