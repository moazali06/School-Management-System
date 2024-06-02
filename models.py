from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.
class CustomUser(AbstractUser):
    USER_CHOICES = (
        (1, 'Admission Office'),
        (2, 'Librarian'),
        (3, 'Teacher'),
        (4, 'Student')
    )
    user_type = models.IntegerField(choices=USER_CHOICES, default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic')

class Subject(models.Model):
    subject_name=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject_name

class Program(models.Model):
    program_name=models.CharField(max_length=50)
    program_fee=models.IntegerField(default=0)
    subjects=models.ManyToManyField(Subject)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.program_name
    
class Session_Year(models.Model):
    session_start=models.CharField(max_length=4)
    session_end=models.CharField(max_length=4)
    programs=models.ManyToManyField(Program)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.session_start+'-'+self.session_end
class Teacher(models.Model):
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    cnic=models.CharField(max_length=15)
    contact=models.CharField(max_length=12)
    address=models.CharField(max_length=100)
    qualification=models.CharField(max_length=20)
    cv=models.FileField(upload_to='education_doc/')
    subjects=models.ManyToManyField(Subject)
    salary=models.IntegerField(default=0)
    def __str__(self):
        return self.admin.first_name+" "+self.admin.last_name

class Parent(models.Model):
    father_name=models.CharField(max_length=50)
    father_cnic=models.CharField(max_length=15)
    father_contact=models.CharField(max_length=12)
    father_email=models.EmailField()
    father_occupation=models.CharField(max_length=30)
    mother_name=models.CharField(max_length=50 ,null=True, default=None)
    mother_cnic=models.CharField(max_length=15 ,null=True, default=None)
    mother_occupation=models.CharField(max_length=30)
    mother_email=models.EmailField()
    mother_contact=models.CharField(max_length=12)
    def __str__(self):
        return f"{self.father_name} "
    
class Educational_Record(models.Model):
    matric_marks=models.CharField(max_length=5)
    inter_marks=models.CharField(max_length=5,null=True, default=None)
    education_doc=models.FileField(upload_to='education_doc/')

class Student(models.Model):
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    roll_no=models.CharField(max_length=10)
    registration_no=models.CharField(max_length=9)
    cnic=models.CharField(max_length=15)
    dob=models.DateField(null=True, default=None)
    gender=models.CharField(max_length=15,null=True, default=None)
    religion=models.CharField(max_length=50,null=True, default=None)
    mobile=models.CharField(max_length=12)
    present_address=models.CharField(max_length=100)
    permanent_address=models.CharField(max_length=100)
    session=models.ForeignKey(Session_Year,on_delete=models.CASCADE)
    program=models.ForeignKey(Program,on_delete=models.CASCADE)
    parent=models.ForeignKey(Parent,on_delete=models.CASCADE)
    img=models.FileField(upload_to='studentpic/')
    educational_record = models.ForeignKey(Educational_Record, on_delete=models.CASCADE, null=True, default=None)
    def __str__(self):
       return self.admin.first_name+" "+self.admin.last_name   

class Student_Fee(models.Model):
    student_id=models.ForeignKey(Student, on_delete=models.CASCADE)
    student_fee=models.CharField(max_length=10)
    semester=models.CharField(max_length=10,default=1)
    fst_installment=models.CharField(max_length=10)
    scnd_installment=models.CharField(max_length=10)
    thrd_installment=models.CharField(max_length=10)
    
    def __str__(self):
        return '{} {} {} {} {}'.format(self.student_id, self.student_fee ,self.fst_installment,self.scnd_installment,
                                       self.thrd_installment
                                       ) 

class Visitor(models.Model):
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE)
    name=models.CharField(max_length=50) 
    cnic=models.CharField(max_length=15)
    contact=models.CharField(max_length=12)
    relation=models.CharField(max_length=50)
    date = models.DateTimeField(default=datetime.now)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.student_id.admin.first_name} {self.student_id.admin.last_name}"

class Books(models.Model):
    book_name=models.CharField(max_length=100)
    author_name=models.CharField(max_length=200)
    publisher_name=models.CharField(max_length=200)
    copies=models.IntegerField(default=0)
    available_copies=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.book_name} - {self.author_name } {self.publisher_name} "

class Laibrary(models.Model):
    student_id=models.ForeignKey(Student, on_delete=models.CASCADE)
    book=models.ForeignKey(Books,on_delete=models.CASCADE, null=True, blank=True)
    date_of_issue=models.DateField()
    date_of_return=models.DateField()
    fine=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class Attendance(models.Model):
    subject_id=models.ForeignKey(Subject,on_delete=models.DO_NOTHING, null=True, blank=True)
    program_id=models.ForeignKey(Program,on_delete=models.CASCADE,null=True, blank=True)
    date=models.DateField(auto_now_add=True)
    session=models.ForeignKey(Session_Year,on_delete=models.DO_NOTHING, null=True, blank=True)
class Attendence_Report(models.Model):
    student_id=models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    attendence_id=models.ForeignKey(Attendance,on_delete=models.CASCADE) 


class Teacher_Leave(models.Model):
    teacher_id=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    date=models.DateField()
    message=models.TextField()
    status=models.IntegerField(default=0)

    def __str__(self):
        return f"{self.teacher_id.admin.first_name+' '+self.teacher_id.admin.last_name} - {self.date}"

class Student_Leave(models.Model):
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE)
    date=models.DateField()
    message=models.TextField()
    status=models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student_id.admin.first_name+' '+self.student_id.admin.last_name} - {self.date}"

class Student_Result(models.Model):
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE,null=True,blank=True)
    subject_id=models.ForeignKey(Subject,on_delete=models.CASCADE)
    assignment_marks=models.IntegerField(default=0)
    midterm_marks=models.IntegerField(default=0)
    exam_marks=models.IntegerField(default=0)
    def __str__(self):
        self.student_id.admin.first_name + ' '+ self.student_id.admin.last_name

class Student_Feedback(models.Model):
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE)
    teacher_id=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    date=models.DateField()
    message=models.TextField()
    

    def __str__(self):
        return f"{self.student_id.admin.first_name+' '+self.student_id.admin.last_name} - {self.teacher_id.admin.first_name+' '+self.teacher_id.admin.last_name}"
