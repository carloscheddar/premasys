from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from reveal.models import Lesson
import ast
import re

def Reveal(request):
    return render_to_response("index.html", RequestContext(request, {'title': 'Test Reveal'}))


def Create(request):
    return render_to_response("create.html", RequestContext(request, {'title': 'Edit'}))


def Save(request):
    post = request.POST.keys()[0]
    page = request.META['HTTP_REFERER'].split('/')
    if page[-1] == 'create':
        Lesson(username=request.user, slide=post).save()
    elif page[-2] == 'edit':
        lesson = get_object_or_404(Lesson, pk=page[-1])
        lesson.slide = post
        lesson.save()
    return render_to_response("save.html", RequestContext(request, {'h': 'hello'}))


def Show(request, lesson_id):
    slide = get_object_or_404(Lesson, pk=lesson_id)
    slide = ast.literal_eval(slide.slide)
    slide = json2html(slide)
    return render_to_response("show.html", RequestContext(request, {'slide': slide}))


def Edit(request, lesson_id):
    slide = get_object_or_404(Lesson, pk=lesson_id)
    slide = ast.literal_eval(slide.slide)
    slide = json2Array(slide)
    return render_to_response("edit.html", RequestContext(request, {'slide': slide}))


# Function to convert json to html to be displayed in show
def json2html(json):
    string = ''
    regex = re.compile("\(([^)]+)\)")
    for j in json:
        t = j["type"]
        text = j["text"]
        if t == "text":
            arr = regex.findall(text)
            string += '<section>'
            for a in arr:
                split = a.split(' ',1)
                if split[0] == "video":
                    split[0] = "iframe";
                    string += "<h1><" + split[0] + " width='420' height='315' src=\'//"+ split[1] +"\'></h1>";
                if split[0] == "img":
                    string += "<h2><" + split[0] + " src=\'"+ split[1] +"\'></h2>";
                    continue;
                string += "<" + split[0] + ">" + split[1] + "</" + split[0] + ">"
            string += '</section>'
        elif t == "question":
            arr = regex.findall(text)
            string += '<section data-state="quiz">'
            for a in arr:
                split = a.split(' ',1)
                if split[0] == "question":
                    split[0] = 'h3'
                if split[0] == "choice":
                    split[0] = 'li'
                if split[0] == "answer":
                    split[0] = 'li'
                    string += "<" + split[0] + " id='answer'>" + split[1] + "</" + split[0] + ">";
                    continue
                string += "<" + split[0] + ">" + split[1] + "</" + split[0] + ">"
            string += '</section>'
    return string


# Converts json to an Array of Plist
def json2Array(json):
    content = []
    string = ''
    regex = re.compile("\(([^)]+)\)")
    for j in json:
        t = j["type"]
        text = j["text"]
        if t == "text" or t == "question":
            arr = regex.findall(text)
            string = ''
            for a in arr:
                string += '(' +a+ ')'
            content.append(string)
    return content
