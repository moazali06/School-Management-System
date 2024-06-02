from django.shortcuts import render,redirect,HttpResponse
from api.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from api.models import *
from datetime import datetime
from django.db.models import Count
from datetime import date
from datetime import datetime, timedelta
from django.db.models import Count, Q
from django.template.loader import get_template
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def Home(request):
    teacher=Teacher.objects.get(admin=request.user.id)
    subjects=teacher.subjects.count()
    context={
        'subjects':subjects
    }
    return render(request,'Teacher/Home.html',context)


def MarkAttendance(request):
        sessions=Session_Year.objects.all()
        programs=Program.objects.all()
        teacher=Teacher.objects.get(admin=request.user.id)
        subjects=teacher.subjects.all()
        student_id = request.POST.get('student_id')
        attendance = request.POST.get('attendance')
        action=request.GET.get('action')

        students=None
        get_subject=None
        get_session=None
        get_program=None 

        if action is not None:
            if request.method=='POST':
                session_id=request.POST.get('session_id')
                program_id=request.POST.get('program_id')
                subject_id=request.POST.get('subject_id')
            
                get_subject=Subject.objects.get(id=subject_id)
                get_session=Session_Year.objects.get(id=session_id)
                get_program=Program.objects.get(id=program_id)

                students=Student.objects.filter(session=get_session, program=get_program)

        context={
            'sessions':sessions,
            'programs':programs,
            'subjects':subjects,
            'get_subject':get_subject,
            'get_session':get_session,
            'get_program':get_program,
            'action':action,
            'students':students
        }
        return render(request,'Teacher/AttendenceSearchStudent.html',context)

def SaveAttendence(request):
    if request.method=='POST':
        subject_id=request.POST.get('subject_id')
        session_id=request.POST.get('session_id')
        date=request.POST.get('date')
        student_id=request.POST.getlist('student_id')
        program_id=request.POST.get('program_id')
        print("this is the program")
        print(program_id)
        print('this is the subject id')
        print(subject_id)
        print('This is the student id ')
        print(student_id)

       
        get_subject=Subject.objects.get(id=subject_id)
        get_session=Session_Year.objects.get(id=session_id)
        get_program=Program.objects.get(id=program_id)
        
        attendence=Attendance(
            subject_id=get_subject,
            date=date,
            session_id=session_id,
            program_id=get_program
        )
        attendence.save()
        for i in student_id:
            stud_id=i
            int_stud=int(stud_id)

            p_students=Student.objects.get(id=int_stud)
            attendence_report=Attendence_Report(
                student_id=p_students,
                attendence_id=attendence
            )
            attendence_report.save()
    return redirect('searchstudentattendence')

def LecturesTaken(request):
    teacher = Teacher.objects.get(admin=request.user.id)
    sessions = Session_Year.objects.all()
    programs = Program.objects.all()
    action = request.GET.get('action')
    get_program = None
    get_session = None
    subjects = None

    if request.method == 'POST':
        session_id = request.POST.get('session')
        program_id = request.POST.get('program')
        subject_id = request.POST.get('subject')

        get_program = get_object_or_404(Program, id=program_id)
        get_session = get_object_or_404(Session_Year, id=session_id)
        subjects = teacher.subjects.all()

        if session_id is not None and program_id is not None and subject_id is not None:
            selected_session = get_object_or_404(Session_Year, id=session_id)
            selected_program = get_object_or_404(Program, id=program_id)
            selected_subject = get_object_or_404(Subject, id=subject_id)

            # Get the total number of lectures taken for the selected subject, session, and program
            total_lectures = Attendance.objects.filter(
                session=selected_session,
                program_id=selected_program,
                subject_id=selected_subject,
            ).count()

            # Get attendance records for each student in the selected subject, session, and program
            students = Attendence_Report.objects.filter(
                attendence_id__session=selected_session,
                attendence_id__program_id=selected_program,
                attendence_id__subject_id=selected_subject
            ).values('student_id').annotate(lectures_attended=Count('attendence_id', distinct=True))

            attendance_data = []
            students_data = []

            for student in students:
                student_id = student['student_id']
                lectures_attended = student['lectures_attended']

                # Calculate the attendance percentage for each student
                if total_lectures > 0:
                    attendance_percentage = (lectures_attended / total_lectures) * 100
                else:
                    attendance_percentage = 0  # To handle division by zero

                # Get student details
                student_details = Student.objects.get(id=student_id)

                # Append data to the attendance_data list
                attendance_data.append({
                    'student_id': student_id,
                    'student_name': student_details.admin.first_name + ' ' + student_details.admin.last_name,
                    'father_name': student_details.parent.father_name,
                    'lectures_attended': lectures_attended,
                    'attendance_percentage': attendance_percentage,
                })

                # Append data to the students_data list
                students_data.append({
                    'student_id': student_id,
                    'name': student_details.admin.first_name + ' ' + student_details.admin.last_name,
                    'father_name': student_details.parent.father_name,
                    'lectures_attended': lectures_attended,
                    'attendance_percentage': attendance_percentage,
                })

            # Get students who haven't attended any lecture
            absent_students = Student.objects.filter(
                ~Q(id__in=[student['student_id'] for student in students]),
                program__id=selected_program.id
            )

            for student in absent_students:
                attendance_data.append({
                    'student_id': student.id,
                    'student_name': student.admin.first_name + ' ' + student.admin.last_name,
                    'father_name': student.parent.father_name,
                    'lectures_attended': 0,
                    'attendance_percentage': 0,
                })

                # Append data to the students_data list for absent students as well
                students_data.append({
                    'student_id': student.id,
                    'name': student.admin.first_name + ' ' + student.admin.last_name,
                    'father_name': student.parent.father_name,
                    'lectures_attended': 0,
                    'attendance_percentage': 0,
                })

            # Store the list in session
            request.session['students_data'] = students_data

            context = {
                'attendance_data': attendance_data,
                'selected_program': selected_program,
                'selected_subject': selected_subject,
                'lectures_taken': total_lectures
            }

            return render(request, 'Teacher/StudentPercentage.html', context)

    context = {
        'sessions': sessions,
        'programs': programs,
        'action': action,
        'get_program': get_program,
        'get_session': get_session,
        'subjects': subjects,
    }

    return render(request, "Teacher/LeacturesTaken.html", context)

def generate_pdf(request):
    # Retrieve the list of student data from session
    students_data = request.session.get('students_data', [])

    # Path to the HTML template file for PDF download
    pdf_template_path = 'Teacher/AttendenceDownloadPDF.html'

    # Render the PDF template with the student data
    pdf_template = get_template(pdf_template_path)
    html = pdf_template.render({'students_data': students_data})

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="StudentPercentage.pdf"'

    # Create PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF')

    return response

def SendTeacherLeave(request):
    if request.method=='POST':
        teacher_id=Teacher.objects.get(admin=request.user.id)
        date=request.POST.get('date')
        message=request.POST.get('leavemessage')

        teachersendleave=Teacher_Leave(
            teacher_id=teacher_id,
            message=message,
            date=date
        )
        teachersendleave.save()
        messages.success(request,'Leave send successfully')
        redirect('teacherhome')
    return render(request,'Teacher/ApplyLeave.html')

def AddResult(request):
    sessions=Session_Year.objects.all()
    programs=Program.objects.all()
    user=CustomUser.objects.get(id=request.user.id)
    teacher=Teacher.objects.get(admin=user)
    subjects=teacher.subjects.all()


    context={
        'subjects':subjects,
        'sessions':sessions,
        'programs':programs
    }
    return render(request,'Teacher/AddResult.html',context)

def SaveResult(request):
    program=request.POST.get('program')
    session=request.POST.get('session')
    students=Student.objects.filter(session=session,program=program)
    subject=request.POST.get('subject')
    # subject=Subject.objects.get(id=subject)
    
    
    
    if request.method=='POST':
        student_id=request.POST.get('student_id')
        assignment_marks=request.POST.get('assignment_marks')
        assignment_marks=int(assignment_marks)
        midterm_marks=request.POST.get('midterm_marks')
        midterm_marks=int(midterm_marks)
        final_marks=request.POST.get('final_marks')
        final_marks=int(final_marks)
        if assignment_marks== None:
            assignment_marks=0
        if midterm_marks== None:
            midterm_marks=0
        if final_marks== None:
            final_marks=0
        result=Student_Result(
            student_id=student_id,
            subject_id=subject,
            assignment_marks=assignment_marks,
            midterm_marks=midterm_marks,
            exam_marks=final_marks
        )
        result.save()
        
    context={
        'students':students,
        
    }
    return render(request,'Teacher/ResultViewStudent.html',context)