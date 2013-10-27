from django.shortcuts import render_to_response
from django.template import RequestContext

def Profile(request):
	return render_to_response("profile.html", RequestContext(request, {'title': 'Premasys Test'}))