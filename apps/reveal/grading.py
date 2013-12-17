from reveal.models import Lesson
import json

# Two sample slides for use as placeholders

#slide = {"type":"question",
#         "question":{"body":"How many meters in a kilometer?",
#                     "choices":["What is a meter?",
#                                "1024, of course.",
#                                "Exactly 1000."],
#                     "answers":["1024, of course.",
#                                "Exactly 1000."]}}
#slide2 = {"type":"question",
#          "question":{"body":"What is the colour of the night?",
#                      "choices":["Sanguine, my brother.",
#                                 "Black.",
#                                 "Diamonds."],
#                      "answers":["Sanguine, my brother."]}}


def LID2key(lessonID):
# Fetch lesson object and return key
    lesson = fetchLesson(lessonID)
    return lesson2key(lesson)


def fetchLesson(lessonID):
# Fetch lesson object
    lesson = Lesson.objects.get(id__exact=lessonID)
    return json.loads(lesson)

# Return the answer key, which is a dictionary of questions
# and correct answers
def lesson2key(lesson):
    # Filter questions from list of slides
    questions = [slide["question"] for slide in lesson 
                 if slide["type"]=="question"]
    # Return key
    return {question["body"]:question["answers"] 
            for question in questions}

# Compare answers to key to get score.
# answers is similar to target: a dictionary of a question
# to a  list of answers.
def score(answers,target):
    grade = 0
    for question in answers:
        grade = grade + compare(answers[question],
                                target[question])
    return grade

# Grade a question
# Provide the option to assign partial points
def compare(answer,target,
            partial=False):
    max_score = len(target)
    wrong = len(list(set(answer)^set(target)))
    score = float(max_score - wrong)/max_score
    if partial:
        return score
    elif wrong > 0:
        return 0
    return 1
