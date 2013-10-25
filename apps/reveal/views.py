from django.shortcuts import render_to_response
from django.template import RequestContext
from reveal.models import Lesson

def Reveal(request):
	return render_to_response("index.html", RequestContext(request, {'title': 'Test Reveal'} ) )

def Edit(request):
  return render_to_response("edit.html", RequestContext(request, {'title': 'Edit'}))