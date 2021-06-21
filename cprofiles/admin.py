from django.contrib import admin
from .models import Student, Mentor, Session, Support, Connection, Tasksubject, Task, Topic, Copytask, Childstrength, Socialstrength, Preferlocation, Mentorlanguage, Question, Topiccalculation, Parentsession

admin.site.register(Student)
admin.site.register(Mentor)
admin.site.register(Connection)
admin.site.register(Session)
admin.site.register(Support)
admin.site.register(Tasksubject)
admin.site.register(Task)
admin.site.register(Topic)
admin.site.register(Copytask)
admin.site.register(Childstrength)
admin.site.register(Socialstrength)
admin.site.register(Preferlocation)
admin.site.register(Mentorlanguage)
admin.site.register(Question)
admin.site.register(Topiccalculation)
admin.site.register(Parentsession)


