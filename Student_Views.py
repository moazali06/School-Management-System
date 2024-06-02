from django.shortcuts import render,redirect,HttpResponse
from api.models import *
from django.contrib import messages

def Home(request):
    return render(request,'Student/Home.html')
def SendStudentLeave(request):
    if request.method=='POST':
        student_id=Student.objects.get(admin=request.user.id)
        date=request.POST.get('date')
        message=request.POST.get('leavemessage')
        print(student_id,message,date)

        studentsendleave=Student_Leave(
            student_id=student_id,
            message=message,
            date=date
        )
        studentsendleave.save()
        
        redirect('studenthome')
    return render(request,'Student/ApplyLeave.html')

def LecturesTaken(request):
    user=CustomUser.objects.get(id=request.user.id)
    student=Student.objects.get(amdin=user)
    session=student.session
    Program=student.program
    action=request.GET.get('action')
    if action is not None:
        pass
def Feedback(request):
    teachers=Teacher.objects.all()
    if request.method=='POST':
        student_id=Student.objects.get(admin=request.user.id)
        teacher_id=request.POST.get('teacher_id')
        teacher=Teacher.objects.get(id=teacher_id)
        date=request.POST.get('date')
        feedback=request.POST.get('feedback')
        print(student_id,feedback,date , teacher)

        studentsendleave=Student_Feedback(
            student_id=student_id,
            teacher_id=teacher,
            date=date,
            message=feedback
        )
        studentsendleave.save()
        
        redirect('studenthome')
    context={
        'teachers':teachers
    }    
    return  render(request,'Student/Feedback.html',context)

