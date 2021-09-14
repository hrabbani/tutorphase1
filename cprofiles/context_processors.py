from .models import *
from django.shortcuts import render


def choice_question(request):

    if(request.user.id):

        choice_unanswered_question_num = Question.objects.filter(status="UNANSWERED").count()

        return {
            'choice_unanswered_question_num' : choice_unanswered_question_num
        }

    return {}

