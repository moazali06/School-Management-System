from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from api.models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
    
@login_required(login_url='/')
def Home(request):
    return render(request, 'Admission/Home.html')

# <===========Student Views==============================>
def AddStudent(request):
    sessions = Session_Year.objects.all()
    programs = Program.objects.all()
    educational_record_id=None 
        # Get Data from Form
    if request.method=="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        cnic = request.POST.get('cnic')
        # other form data retrieval here...
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        program_id = request.POST.get('program')
        relegion = request.POST.get('relegion')
        session_id = request.POST.get('session')
        mobile = request.POST.get('mobile')
        registration_no = request.POST.get('reg_no')
        student_email = request.POST.get('student_email')
        father_name = request.POST.get('father_name')
        father_cnic = request.POST.get('father_cnic')
        father_occupation = request.POST.get('father_occupation')
        father_contact = request.POST.get('father_contact')
        father_email = request.POST.get('father_email')
        mother_name = request.POST.get('mother_name')
        mother_cnic = request.POST.get('mother_cnic')
        mother_occupation = request.POST.get('mother_occupation')
        mother_contact = request.POST.get('mother_contact')
        mother_email = request.POST.get('mother_email')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')
        roll_no=request.POST.get('roll_no')
        img=request.FILES.get('image')
        username=request.POST.get('username')
        password=request.POST.get('password')

        # Checking Student Exist or Not
        if Student.objects.filter(cnic=cnic).exists():
            messages.warning(request, 'Student with the same CNIC already exists')
            return redirect('addstudent')
         # Retrieve marks data
        try:
            ttl_mrks = int(request.POST.get('ttl_mrks'))
            obt_mrks = int(request.POST.get('obt_mrks'))
        except ValueError:
            messages.error(request, 'Invalid marks provided')
            return redirect('addstudent')

         # Calculate percentage
        if ttl_mrks <= 0:
            messages.error(request, 'Total marks must be a positive integer')
            return redirect('addstudent')

        percent = (obt_mrks * 100) / ttl_mrks
         # Determine student fee based on percentage
        if percent < 0 or percent > 100:
            messages.error(request, 'Percentage must be between 0 and 100')
            return redirect('addstudent')
        elif percent >= 70 and percent < 80:
            student_fee_percent = 50
        elif percent >= 80 and percent < 90:
            student_fee_percent = 60
        elif percent >= 90:
            student_fee_percent = 70
        else:
            student_fee_percent = 100
        
        # Check if parent already exists
        if Parent.objects.filter(father_cnic=father_cnic).exists():
            parent = Parent.objects.get(father_cnic=father_cnic)
            # If parent exists, get its id
            parent_id = parent.id
        else:
        # If parent does not exist, create new parent instance
            parent = Parent.objects.create(
                father_name=father_name,
                father_cnic=father_cnic,
                father_occupation=father_occupation,
                father_contact=father_contact,
                father_email=father_email,
                mother_name=mother_name,
                mother_cnic=mother_cnic,
                mother_occupation=mother_occupation,
                mother_contact=mother_contact,
                mother_email=mother_email
            )
            # Get the id of newly created parent
        parent_id = parent.id
            # Create new educational_record instance
        educational_record = Educational_Record.objects.create(
            inter_marks=obt_mrks
        )
            # Get the id of the newly created educational_record
        educational_record_id = educational_record.id
        #   Save Data to Custom User 
        user=CustomUser(
            first_name=first_name,
            last_name=last_name,
            email=student_email,
            username=username,
            profile_pic=img,
            user_type=4
        )
        user.set_password(password)
        user.save()
        #   Save Data in Student Model
        student = Student.objects.create(
            admin=user,
            cnic=cnic,
            gender=gender,
            dob=dob,
            roll_no=roll_no,
            program_id=program_id,
            religion=relegion,
            session_id=session_id,
            mobile=mobile,
            registration_no=registration_no,
            present_address=present_address,
            permanent_address=permanent_address,
            parent_id=parent_id , # Assign parent id
            img=img,
            educational_record=educational_record  # Pass the instance directly
        )
        # Save the student
        student.save()
        # Calculate student fee
        program = Program.objects.get(id=program_id)
        program_fee = program.program_fee
        student_fee = (program_fee * student_fee_percent) / 100
        sports_fee=400
        examination_fee=5000
        student_fee=student_fee+examination_fee+sports_fee
        installments=student_fee/3
         # Create student fee instance
        student_fee_instance = Student_Fee.objects.create(
            student_id=student,
            student_fee=student_fee,
            fst_installment=installments,
            scnd_installment=installments,
            thrd_installment=installments
        )
         # Save the student fee
        student_fee_instance.save()

        # Additional processing...
        messages.success(request, 'Student saved successfully')
        return redirect('addstudent')
        
    context = {
        'programs': programs,
        'sessions': sessions
    }
    return render(request,'Admission/StudentAdd.html',context)

def SearchStudent(request):
    if request.method=='POST':
        std_cnic1=request.POST.get('std_cnic_part1')
        std_cnic2=request.POST.get('std_cnic_part2')
        std_cnic3=request.POST.get('std_cnic_part3')
        student = get_object_or_404(Student,cnic=std_cnic1+'-'+std_cnic2+'-'+std_cnic3)
        context={
            "student":student
        }
        return render(request,'Admission/StudentView.html',context)
    return render(request,'Admission/StudentSearch.html')

def EditStudent(request,id):
    student=Student.objects.get(id=id)
    educational_record = student.educational_record
    print(educational_record)
    session=Session_Year.objects.all()
    program=Program.objects.all()
    print(student)
    context={
            "student":student,
            'programs':program,
            "sessions":session,
            'educational_record':educational_record

        }
        
    return render(request,'Admission/StudentEdit.html',context)

def UpdateStudent(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        parent_id = request.POST.get('parent_id')
        print(student_id,parent_id)

        # Retrieve the student object or raise a 404 error if it doesn't exist
        user = CustomUser.objects.get(id=student_id)
        student=Student.objects.get(admin=student_id)
        # Retrieve the parent object or raise a 404 error if it doesn't exist
        parent = get_object_or_404(Parent, id=parent_id)

        # Update student fields
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        student.cnic = request.POST.get('cnic')
        student.gender = request.POST.get('gender')
        student.dob = request.POST.get('dob')
        # Retrieve and validate program
        program_id = request.POST.get('program')
        program = get_object_or_404(Program, id=program_id)
        student.program = program
        # Retrieve and validate session year
        session_id = request.POST.get('session')
        session_year = get_object_or_404(Session_Year, id=session_id)
        print(session_id)
        student.session = session_year
        student.religion = request.POST.get('relegion')
        student.mobile = request.POST.get('mobile')
        student.registration_no = request.POST.get('reg_no')
        user.email = request.POST.get('student_email')
        student.present_address = request.POST.get('present_address')
        student.permanent_address = request.POST.get('permanent_address')

        # Update parent fields
        parent.father_name = request.POST.get('father_name')
        parent.father_cnic = request.POST.get('father_cnic')
        parent.father_occupation = request.POST.get('father_occupation')
        parent.father_contact = request.POST.get('father_contact')
        parent.father_email = request.POST.get('father_email')
        parent.mother_name = request.POST.get('mother_name')
        parent.mother_cnic = request.POST.get('mother_cnic')
        parent.mother_occupation = request.POST.get('mother_occupation')
        parent.mother_contact = request.POST.get('mother_contact')
        parent.mother_email = request.POST.get('mother_email')

        
         
        # Save user,student and parent objects
       
        user.save()
        student.save()
        parent.save()

        return redirect('searchstudent')
    return render(request, 'Admission/StudentSearch.html')

def DeleteStudent(request,id):
    student_id=Student.objects.get(id=id)
    student_id.delete()
    return render(request,"Admission/StudentSearch.html")

# <===========Teacher Views==============================>
def AddTeacher(request):
    subjects = Subject.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        cnic = request.POST.get('cnic')
        contact = request.POST.get('contact_no')
        email = request.POST.get('email')
        address = request.POST.get('address')
        qualification = request.POST.get('qualification')
        cv = request.POST.get('cv')
        username=request.POST.get('username')
        password=request.POST.get('password')
        subject_names = request.POST.getlist('subject')  # Use getlist to get multiple selected subjects
        print(email,password)

         #   Save Data to Custom User 
        user=CustomUser(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            user_type=3
        )
        user.set_password(password)
        user.save()
         # Create the teacher with the given name
        teacher = Teacher.objects.create( admin=user,cnic=cnic, address=address, qualification=qualification, cv=cv, contact=contact)

         # Get Subject instances based on their names and add them to the teacher
        subjects_to_add = Subject.objects.filter(subject_name__in=subject_names)
        teacher.subjects.set(subjects_to_add)

        messages.success(request, 'Teacher Added Successfully')
        return redirect('addteacher')
        
    context = {
        'subjects': subjects
    }
    return render(request,'Admission/TeacherAdd.html',context)

def SearchTeacher(request):
    if request.method=='POST':
        std_cnic1=request.POST.get('std_cnic_part1')
        std_cnic2=request.POST.get('std_cnic_part2')
        std_cnic3=request.POST.get('std_cnic_part3')
        teacher = get_object_or_404(Teacher,cnic=std_cnic1+'-'+std_cnic2+'-'+std_cnic3)
        context={
            "teacher":teacher
        }
        return render(request,'Admission/TeacherView.html',context)
    return render(request,'Admission/TeacherSearch.html')

def EditTeacher(request,id):
    teacher=Teacher.objects.get(id=id)
    subjects=Subject.objects.all()
    
      

    context={
        'teacher':teacher,
        'subjects':subjects
    }
    return render(request,'Admission/TeacherEdit.html',context)

def UpdateTeacher(request):
    if request.method=='POST':
        teacher_id=request.POST.get('teacher_id')
        subject_ids = request.POST.getlist('subject_name[]')  # Use getlist() to get multiple values
        user=CustomUser.objects.get(id=teacher_id)
        teacher=Teacher.objects.get(admin=teacher_id)

        user.first_name=request.POST.get('first_name')
        user.last_name=request.POST.get('last_name')
        teacher.cnic=request.POST.get('cnic')
        teacher.address=request.POST.get('address')
        user.email=request.POST.get('email')
        teacher.contact=request.POST.get('contact_no')
        teacher.qualification=request.POST.get('qualification')

        
        if 'cv' in request.FILES:
            teacher.cv = request.FILES['cv']
        user.save()
        teacher.save()
        teacher.subjects.clear()
        teacher.subjects.add(*subject_ids)  # Fix the typo here, it should be `add` not `aadd`
        return redirect('searchteacher')  # Redirect to the list of programs

        
    return render(request,'Admission/TeacherSearch.html')

def DeleteTeacher(request,id):
    teacher_id=Teacher.objects.get(id=id)
    teacher_id.delete()
    return redirect('searchteacher')

# <===========Session-Year Views===========================>

def AddSessionYear(request):
    programs = Program.objects.all()

    if request.method == 'POST':
        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end')
        program_names = request.POST.getlist('program')

        # Create the session
        session = Session_Year.objects.create(session_start=session_start, session_end=session_end)

        # Get Program instances based on their names and add them to the session
        programs_to_add = Program.objects.filter(program_name__in=program_names)
        session.programs.set(programs_to_add)

        messages.success(request, 'Session-Year Added Successfully')
        return redirect('addsessionyear')

    context = {
        'programs': programs,
    }
    return render(request,'Admission/Session-YearAdd.html',context)

def ViewSessionYear(request):
    sessions=Session_Year.objects.all()
    context={
                "sessions":sessions
        }
    return render(request,'Admission/Session-YearView.html',context)

def EditSessionYear(request,id):
    programs = Program.objects.all()
    session = Session_Year.objects.get(id=id)
    selected_program_ids = [program.id for program in session.programs.all()]  # Get IDs of selected programs

    context = {
        'programs': programs,
        'session': session,
        'selected_program_ids': selected_program_ids,  # Pass the selected program IDs to the template
    }
    return render(request,'Admission/Session-YearEdit.html',context)

def UpdateSessionYear(request):
    if request.method == 'POST':
        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end')
        program_ids = request.POST.getlist('program_name[]')
        session_id=request.POST.get("session_id")
        session_year = Session_Year.objects.get(id=session_id)
        session_year.session_start = session_start
        session_year.session_end = session_end
        session_year.save()

        session_year.programs.clear()
        session_year.programs.add(*program_ids)

        return redirect('viewsessionyear')  # Redirect to session list page
    else:
        session = Session_Year.objects.get(id=id)
        programs = session.programs.all()

        context = {
            'session': session,
            'programs': programs,
        }
    return render(request,'Admssion/Session-YearView.html',context)

def DeleteSessionYear(request,id):
    sessionyear_id=Session_Year.objects.get(id=id)
    sessionyear_id.delete()
    return redirect('viewsessionyear')
# <===========Program Views===========================>

def AddProgram(request):
    subjects = Subject.objects.all()

    if request.method == 'POST':
        program_name = request.POST.get('program_name')
        subject_names = request.POST.getlist('subject')
        program_fee= request.POST.get('program_fee')
       
        # Create the program with the given name
        program = Program.objects.create(program_name=program_name)

        # Get Subject instances based on their names and add them to the program
        subjects_to_add = Subject.objects.filter(subject_name__in=subject_names)
        program.subjects.set(subjects_to_add)
        messages.success(request, 'Programs are added successfully.')
        return redirect('addprogram')


    context = {
        'subjects': subjects,
    }
    return render(request,'Admission/ProgramAdd.html',context)

def ViewProgram(request):
    programs=Program.objects.all()
    context={
        'programs':programs
    }
    return render(request,'Admission/ProgramView.html',context)

def EditProgram(request,id):
    program=Program.objects.get(id=id)
    subjects=Subject.objects.all()
    context={
        'programs':program,
        'subjects':subjects
    }
    
    return render(request,'Admission/ProgramEdit.html',context)
def UpdateProgram(request):
    if request.method == "POST":
        program_id = request.POST.get('program_id')
        program_name = request.POST.get('program_name')
        program_fee = request.POST.get('program_fee')
        subject_ids = request.POST.getlist('subject_name[]')  # Use getlist() to get multiple values
        program = Program.objects.get(id=program_id)
        program.program_name = program_name
        program.program_fee = program_fee
        program.save()
        program.subjects.clear()
        program.subjects.add(*subject_ids)  # Fix the typo here, it should be `add` not `aadd`

        return redirect('viewprogram')  # Redirect to the list of programs
    else:
        program_id = request.POST.get('program_id')  # Corrected to request.POST
        programs = Program.objects.get(id=program_id)
        subjects = programs.subjects.all()
        context = {
            'programs': programs,
            'subjects': subjects
        }
        return render(request, "Admission/ProgramEdit.html", context)

# <===========Subject Views===========================>    

def AddSubject(request):
    if request.method=='POST':
        subject_name=request.POST.get('subject_name')
        print(subject_name)
        subject=Subject.objects.create(
            subject_name=subject_name
        )
        return redirect('addsubject')
    return render(request,'Admission/SubjectAdd.html')

def ViewSubject(request):
    subject=Subject.objects.all()
    context={
        'subjects':subject
    }
    
    return render(request,'Admission/SubjectView.html',context)

def EditSubject(request,id):
    subject=Subject.objects.get(id=id)
    context={
        'subject':subject
    }
    return render(request,'Admission/SubjectEdit.html',context)

def UpdateSubject(request):
    if request.method=='POST':
        subject_id=request.POST.get('subject_id')
        subject_name=request.POST.get('subject_name')

        subject=Subject.objects.get(id=subject_id)
        subject.subject_name=subject_name
        subject.save()
        return redirect('viewsubject')
    return render(request,'Admission/SubjectView.html')

def DeleteSubject(request,id):
    subject_id=Subject.objects.get(id=id)
    subject_id.delete()
    return redirect('viewsubject')


# <===========Visitor Views==============================>
def AddVisitor(request):
    programs=Program.objects.all()
    sessions=Session_Year.objects.all()

    if request.method=='POST':
        session_id=request.POST.get('session')
        program_id=request.POST.get('program')
        student_name=request.POST.get('student_name')
        student=Student.objects.filter(
            admin__first_name__icontains=student_name,
            program_id=program_id,
            session_id=session_id
        )
        context={
            'session':sessions,
            'programs':programs,
            'students':student
        }
        return render(request,'Admission/VisitorViewStudent.html',context)

    context={
        'programs':programs,
        'sessions':sessions
    }
    return render(request,'Admission/VisitorAdd.html',context)

def AddVisitorInfo(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        messages.error(request, 'Student does not exist.')
        return redirect('searchstudent')

    if request.method == 'POST':
        visitor_name = request.POST.get('visitor_name')
        visitor_cnic = request.POST.get('visitor_cnic')
        visitor_relation = request.POST.get('visitor_relation')
        visitor_contact = request.POST.get('visitor_contact')

        # To save the Visitor Information
        visitor = Visitor.objects.create(
            student_id=student,  # Pass the student object directly
            name=visitor_name,
            cnic=visitor_cnic,
            contact=visitor_contact,
            relation=visitor_relation,
            date=datetime.now(),
        )
        messages.success(request, 'Visitor added successfully.')
        return redirect('addvisitor')  # Redirect to appropriate page

    return render(request, 'Admission/Visitor_Information.html', {'student': student})
def ViewVisitor(request):
    visitors=Visitor.objects.all()

    context={
        'visitors':visitors
    }
    return render(request,'Admission/VisitorView.html',context)



def AddLaibrarian(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
       

         #   Save Data to Custom User 
        user=CustomUser(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            user_type=2
        )
        user.set_password(password)
        user.save()
        
        messages.success(request, 'Laibrarian Added Successfully')
        return redirect('addlaibrarian')
        
    return render(request,'Admission/LaibrarianAdd.html')    
# <===========Leave Views==============================>
def TeacherLeaveView(request):

    teacherleave=Teacher_Leave.objects.all()

    context={
        'teacherleaves':teacherleave
    }
    return render(request,'Admission/TeacherLeaveView.html',context)

def Teacher_LeaveApprove(request,id):
    leave=Teacher_Leave.objects.get(id=id)
    leave.status=1
    leave.save()
    return redirect('teacherleaveview')

def Teacher_LeaveDisapprove(request,id):
    leave=Teacher_Leave.objects.get(id=id)
    leave.status=2
    leave.save()
    return redirect('teacherleaveview')

def StudentLeaveView(request):

    studentleave=Student_Leave.objects.all()

    context={
        'studentleaves':studentleave
    }
    return render(request,'Admission/StudentLeaveView.html',context)

def Student_LeaveApprove(request,id):
    leave=Student_Leave.objects.get(id=id)
    leave.status=1
    leave.save()
    return redirect('studentleaveview')

def Student_LeaveDisapprove(request,id):
    leave=Student_Leave.objects.get(id=id)
    leave.status=2
    leave.save()
    return redirect('studentleaveview')
    
# <===========Feedback Views==============================>

def StudentFeedback(request):
    student_feedback=Student_Feedback.objects.all()
    context={
        'student_feedback':student_feedback
    }
    return render(request,'Admission/StudentFeedback.html',context)