from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from registration.models import User


def Common(request):
<<<<<<< HEAD
    return render_to_response("base.html", RequestContext(request, {'title': 'Premasys Test'}))
=======
	try:
		user = User.objects.get( username=request.user)
	except:
		user = ''
	return render_to_response("base.html", RequestContext(request, {'user': user} ) )
>>>>>>> 18d1f9d7e5f5b37ddeda8ca1849a4651fe8556d5
