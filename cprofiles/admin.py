from django.contrib import admin
from .models import Student, Mentor, Session, Support, Connection, Tasksubject, Task, Topic, Copytask

admin.site.register(Student)
admin.site.register(Mentor)
admin.site.register(Connection)
admin.site.register(Session)
admin.site.register(Support)
admin.site.register(Tasksubject)
admin.site.register(Task)
admin.site.register(Topic)
admin.site.register(Copytask)



