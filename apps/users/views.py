from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from registration.models import User
from reveal.models import Lesson

def Profile(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	try:
		lesson = Lesson.objects.get(username=user).slide
	except:
		lesson = ''
	return render_to_response("users/profile.html", RequestContext(request, {
		'title': 'Profile',
		'user_page' : user,
		'lesson' : lesson
		}))