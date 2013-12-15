from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth import login
from forms import MoodleForm
from registration.models import User
from registration.backends.simple.views import RegistrationView
from django.http import HttpResponseRedirect
from django.contrib import messages

import bcrypt
import os
import requests


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
        try:
            api = requests.get(moodleUrl, params=payload).json()[0]
            salt = api['password'].encode('utf-8')
            email = api['email']

            #Check if the user and password match with moodle
            if clean(password, salt):
                authenticated = True

                #Check if the user is in the local database and if the password matches
                new_user = authenticate(username=username, password=password)

                #Check if the username exists
                user = get_object_or_404(User, username=username)

                #If the user exists, is authenticated but wrong password
                #then the username exists in our database.
                if authenticated and new_user is None and user:
                    messages.error(request, "Username already in local database")
                    return MoodleLogin(request)

                #Login the user with moodle
                if new_user:
                    login(request, new_user)

                #If this is the first moodle login then register the user
                else:
                    reg = RegistrationView()
                    data = {'username': username,
                            'email': email,
                            'password1': password}
                    #Register the user and log him in
                    reg.register(request, **data)

            #Username in moodle but wrong password
            else:
                messages.error(request, "Invalid moodle credentials")
                return MoodleLogin(request)

        #Username not in moodle
        except:
            messages.error(request, "Username not in our moodle database")
            return MoodleLogin(request)

    return HttpResponseRedirect('/')


def MoodleLogin(request):
    form = MoodleForm()
    form.is_valid()
    return render_to_response("moodle_login.html", RequestContext(request, {'form': form}))


#Function to verify if the given password matches the moodle password
def clean(password, salt):
    if(bcrypt.hashpw(password, salt) == salt):
        return True
    return False
