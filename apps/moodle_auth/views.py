from django.shortcuts import render_to_response
from django.template import RequestContext

from forms import MoodleForm
import bcrypt
import os
import requests
from registration.models import User


def Authenticate(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password'].encode('utf-8')
        email = None
        authenticated = False

        #Setup request url and parameter for API
        moodleUrl = os.environ['MOODLE_API_URL']
        payload = {'username': username}

        #Get values from the API
        api = requests.get(moodleUrl, params=payload).json()[0]
        salt = api['password'].encode('utf-8')
        email = api['email']

        #Check if the user and password match with moodle
        if clean(password, salt):
            authenticated = True


    return render_to_response("moodle_auth.html", RequestContext(request, {'username': username,
                                                                           'email': email,
                                                                           'auth': authenticated} ) )


def MoodleLogin(request):
    form = MoodleForm()
    form.is_valid()
    return render_to_response("moodle_login.html", RequestContext(request, {'form': form} ) )


#Function to verify if the given password matches the moodle password
def clean(password, salt):
    if(bcrypt.hashpw(password, salt) == salt):
        return True
    return False