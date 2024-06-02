from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class UserModel(UserAdmin):
    list_display=['username','user_type']
admin.site.register(CustomUser,UserModel)
admin.site.register(Subject)
admin.site.register(Program)
admin.site.register(Session_Year)
admin.site.register(Student)
admin.site.register(Student_Fee)
admin.site.register(Parent)
admin.site.register(Teacher)
admin.site.register(Visitor)
admin.site.register(Books)
admin.site.register(Laibrary)
admin.site.register(Attendance)
admin.site.register(Teacher_Leave)
admin.site.register(Student_Leave)
admin.site.register(Student_Feedback)
admin.site.register(Student_Result)

