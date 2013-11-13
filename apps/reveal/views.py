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

#
def Save_Lesson(lesson):
	ID = lesson["LessonID"]
	#Lesson(LessionId = ID).save()
	for slide in lesson["Slides"]:
		Slides(LessonID = ID, Number = slide["Number"]).save()
		
		for content in slide["Content"]:
			Content(SlideID=slide["SlideID"], Type = content["Type"], Data = content["Data"]).save()

	return lesson


####GET FUNCTIONS####

#
def Get_All_Answers(Q_ID):
	answers = Answers.objects.all().filter(QuestionID = Q_ID)
	return answers

#
def Get_Question(C_ID):
	question = Question.objects.filter(ContentID = C_ID)
	question["answers"]= Get_All_Answers(question["QuestionID"])#access question correctly

	return question

#
def Get_All_Content(S_ID):
	content = sorted(Content.objects.all().filter(SlideID = S_ID), key = lambda item: item["Number"])

	return content

#
def Get_All_Slides(L_ID):
	slides = sorted(Slides.objects.all().filter(LessonID = L_ID), key =lambda item: item['Number'])

	for sl in slides:
		slides["Content"] = Get_All_Content(sl["S_ID"])
	
	return slides

#
def Get_Subject(L_ID):
	subject = Subject.objects.all().filter(LessonID_ L_ID)
	return subject

#
def Get_Lesson(L_ID):
	lesson = Lesson.objects.filter(LessonID = L_ID)
	lesson["Slides"] = Get_All_Slides(L_ID)
	lesson["Subject"] = Get_Subject(L_ID)

	return lesson

	
### VIEW A COURSE OR LESSON FUNCTIONS

#
def Permit_View(C_ID, U_ID):
	Check_Course = User_Course.objects.filter(CourseID = C_ID, UserID = U_ID)
	if():#check if relation user to course exists
		return (True, Check_Course["PermEdits"]) #If it does exist return the True and the permit value
	else:#there is no relation
		return (False, False)

#
def Permit_Edit(C_ID, U_ID):
	Check_Course = User_Course.objects.filter(CourseID = C_ID, UserID = U_ID)
	if(): #check if relation user to course exists
		return Check_Course["PermEdits"]) #If it does exist return the permit value
	else: #there is no relation
		return False
