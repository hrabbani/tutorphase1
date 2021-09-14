from .models import *
from django.shortcuts import render


def middle_school_question(request):

    if(request.user.id):

        middle_school_unanswered_question_num = Question.objects.filter(status="UNANSWERED").count()

        return {
            'middle_school_unanswered_question_num' : middle_school_unanswered_question_num
        }

    return {}

