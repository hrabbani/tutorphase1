from .models import *
from django.shortcuts import render


def mentor_question(request):

    if(request.user.id):

        mentor_unanswered_question_num = Question.objects.filter(status="UNANSWERED").count()

        return {
            'mentor_unanswered_question_num' : mentor_unanswered_question_num
        }

    return {}

