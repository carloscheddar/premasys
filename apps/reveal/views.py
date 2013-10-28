from django.shortcuts import render_to_response
from django.template import RequestContext
from reveal.models import Lesson

def Reveal(request):
	return render_to_response("index.html", RequestContext(request, {'title': 'Test Reveal'} ) )

def Edit(request):
  return render_to_response("edit.html", RequestContext(request, {'title': 'Edit'}))

def Save(request):
	print request.POST
	print request.user
	Lesson(username=request.user, slide=request.POST)
	return render_to_response("save.html", RequestContext(request,{'h': 'hello'}))