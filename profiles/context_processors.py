from .models import *
from django.shortcuts import render


def high_school_question(request):

    if(request.user.id):

        high_school_unanswered_question_num = Question.objects.filter(status="UNANSWERED").count()

        return {
            'high_school_unanswered_question_num' : high_school_unanswered_question_num
        }

    return {}

