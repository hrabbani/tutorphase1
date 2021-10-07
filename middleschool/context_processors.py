from .models import *
from django.shortcuts import render


def middle_school_question(request):

    if(request.user.id):

        middle_school_unanswered_question_num = Question.objects.filter(status="UNANSWERED").count()
        middle_school_session_flag_num = Session.objects.filter(flag=True).count()


        return {
            'middle_school_unanswered_question_num' : middle_school_unanswered_question_num,
            'middle_school_session_flag_num' : middle_school_session_flag_num
        }

    return {}

