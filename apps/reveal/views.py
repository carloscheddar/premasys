from django.shortcuts import render_to_response
from django.template import RequestContext
def Reveal(request):
	return render_to_response("index.html", RequestContext(request, {'title': 'Test Reveal'} ) )