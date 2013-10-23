from django.shortcuts import render_to_response
from django.template import RequestContext


def Common(request):
  return render_to_response("base.html", RequestContext(request, {'title': 'Premasys Test'} ) )

def Login(request):
  return render_to_response("login.html", RequestContext(request, {'title': 'Premasys Test'} ) )