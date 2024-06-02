"""
URL configuration for BrainBoster project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


from . import Admission_Office_Views, views,Laibrary_Views,Teacher_Views,Student_Views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('base',views.Base,name='base'),

    # <===================Login=======================================>
    path('',views.Login,name='login'),
    path('dologin',views.DoLogin,name='dologin'),
    path('admission/home',Admission_Office_Views.Home,name="admissionhome"),
    path('laibrary/home',Laibrary_Views.Home,name='laibrarianhome'),
    path('teacher/home',Teacher_Views.Home,name='teacherhome'),
    path('student/home',Student_Views.Home,name='studenthome'),
    
      # <===================Logout=======================================>
    path('dologout',views.DoLogOut,name='dologout'),

    # <===================Profile Update=======================================>
    path('profile',views.Profile,name='profile'),
    path('update/profile',views.UpdateProfile,name='profileupdate'),
      
      # <===================Add Laibrarian=======================================>  
        path('add/laibrarian',Admission_Office_Views.AddLaibrarian,name='addlaibrarian'),
      # <===================Admission Office URLS=======================================>

                        #<-----Student URLS---->
    path('add/student',Admission_Office_Views.AddStudent,name="addstudent"),
    path('search/student',Admission_Office_Views.SearchStudent,name='searchstudent'),
    path('edit/student/<int:id>',Admission_Office_Views.EditStudent,name='editstudent'),
    path('update/student',Admission_Office_Views.UpdateStudent,name='updatestudent'),
    path('delete/student/<int:id>',Admission_Office_Views.DeleteStudent,name='deletestudent'),

                        #<-----Teacher URLS---->
    path('add/teacher',Admission_Office_Views.AddTeacher,name='addteacher'),
    path('search/teacher',Admission_Office_Views.SearchTeacher,name='searchteacher'),
    path('edit/teacher/<int:id>',Admission_Office_Views.EditTeacher,name='editteacher'),
    path('update/teacher',Admission_Office_Views.UpdateTeacher,name='updateteacher'),
    path('delete/teacher/<int:id>',Admission_Office_Views.DeleteTeacher,name='deleteteacher'),
                        #<-----Session-Year URLS---->
    path('add/sessionyear',Admission_Office_Views.AddSessionYear,name='addsessionyear'),
    path('view/sessionyear',Admission_Office_Views.ViewSessionYear,name='viewsessionyear'),
    path('edit/sessionyear/<int:id>',Admission_Office_Views.EditSessionYear,name='editsessionyear'),
    path('update/sessionyear',Admission_Office_Views.UpdateSessionYear,name='updatesessionyear'),
    path('delete/sessionyear/<int:id>',Admission_Office_Views.DeleteSessionYear,name='deletesessionyear'),
                        #<-----Program URLS---->
    path('add/program',Admission_Office_Views.AddProgram,name='addprogram'),
    path('view/program',Admission_Office_Views.ViewProgram,name='viewprogram'),
    path('edit/program/<int:id>',Admission_Office_Views.EditProgram,name='editprogram'),
    path('update/program',Admission_Office_Views.UpdateProgram,name='updateprogram'),
    # path('delete/program/<int:id>',Admission_Office_Views.DeleteSubject,name='deleteprogram'),
                         #<-----Subject URLS---->
    path('add/subject',Admission_Office_Views.AddSubject,name='addsubject'),
    path('view/subject',Admission_Office_Views.ViewSubject,name='viewsubject'),
    path('edit/subject/<int:id>',Admission_Office_Views.EditSubject,name='editsubject'),
    path('update/subject',Admission_Office_Views.UpdateSubject,name='updatesubject'),
    path('delete/subject/<int:id>',Admission_Office_Views.DeleteSubject,name='deletesubject'),
                         #<-----Visitor URLS---->
    path('add/visitor',Admission_Office_Views.AddVisitor,name='addvisitor'),
    path('add/visitorinfo/<int:id>', Admission_Office_Views.AddVisitorInfo,name='addvisitorinfo'),
    path('view/visitor',Admission_Office_Views.ViewVisitor,name='viewvisitor'),
                        #<-----Teacher Leave URLS---->
    path('teacher/leave/view',Admission_Office_Views.TeacherLeaveView,name='teacherleaveview'),
    path('teacher/leave/approve/<str:id>',Admission_Office_Views.Teacher_LeaveApprove,name='teacherleaveapprove'),
     path('teacher/leave/disapprove/<str:id>',Admission_Office_Views.Teacher_LeaveDisapprove,name='teacherleavedisapprove'),

                         #<-----Student Leave URLS---->
    path('student/leave/view',Admission_Office_Views.StudentLeaveView,name='studentleaveview'),
    path('student/leave/approve/<str:id>',Admission_Office_Views.Student_LeaveApprove,name='studentleaveapprove'),
     path('student/leave/disapprove/<str:id>',Admission_Office_Views.Student_LeaveDisapprove,name='studentleavedisapprove'),
                        #<-----Feedback URLS---->
    path('view/student/feedback',Admission_Office_Views.StudentFeedback,name='viewstudentfeedback'),

     # <===================Laibrary URLS=======================================>
     path('add/book',Laibrary_Views.AddBook,name='addbook'),
     path('search/book',Laibrary_Views.SearchBook,name='searchbook'),
     path('issue/book/<int:id>',Laibrary_Views.IssueBook,name='issuebook'),
     path('retrun/book',Laibrary_Views.ReturnBook,name='returnbook'),
     path('fine/cleared/<int:id>',Laibrary_Views.FineCleared,name='finecleared'),

     # <===================Teacher URLS=======================================>
                         #<-----Attendence URLS---->
                
      path('attendence/search/student',Teacher_Views.MarkAttendance,name='searchstudentattendence'),                  
      path('attendence/mark',Teacher_Views.SaveAttendence,name='saveattendence'),
      path('lectures/taken', Teacher_Views.LecturesTaken,name='lecturestaken' ),
      path('teacher/send/leave',Teacher_Views.SendTeacherLeave,name='sendteacherleave'),
      path('generate_pdf/', Teacher_Views.generate_pdf, name='generate_pdf'),
                            #<-----Result URLS---->
      path('add/result',Teacher_Views.AddResult,name='addresult'),
      path('save/result',Teacher_Views.SaveResult,name='saveresult'),

      # <===================Student URLS=======================================>  
                        #<-----Attendence URLS---->
                       
      path('student/send/leave',Student_Views.SendStudentLeave,name='sendstudentleave'),
                      #<-----Feedback URLS---->      
      path('sendtecher/feedback',Student_Views.Feedback,name='sendteacherfeedback'),                
     
      # <==========================================================>  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

