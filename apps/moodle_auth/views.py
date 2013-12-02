from django.shortcuts import render_to_response
from django.template import RequestContext

from forms import MoodleForm
import subprocess
import MySQLdb
import bcrypt
import os
from registration.models import User


commands = ['ssh', '-N', '-L',
            os.environ['toFromBind'],
            os.environ['sshServer']]

def Authenticate(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password'].encode('utf-8')
        email = None
        authenticated = False
    try:
        myDB = MySQLdb.connect(db="moodle",
                               host=os.environ['moodle_host'],
                               port=int(os.environ['moodle_port']),
                               user=os.environ['moodle_user'],
                               passwd=os.environ['moodle_password'])

        cursor = myDB.cursor()

        cursor.execute("select * from mdl_user where username = '%s';" % username)

        cursor = cursor.fetchall()[0]

        salt = cursor[8]
        email = cursor[12]

        if clean(password, salt):
            authenticated = True
            print authenticated

    except MySQLdb.OperationalError:
        subprocess.Popen(commands, stdin=None, stdout=None, stderr=None, close_fds=True)
        print "Opening connection"

    return render_to_response("moodle_auth.html", RequestContext(request, {'username': username,
                                                                           'email': email,
                                                                           'auth': authenticated} ) )


def MoodleLogin(request):
    form = MoodleForm()
    form.is_valid()
    return render_to_response("moodle_login.html", RequestContext(request, {'form': form} ) )


def clean(password, salt):
    if(bcrypt.hashpw(password, salt) == salt):
        return True
    return False