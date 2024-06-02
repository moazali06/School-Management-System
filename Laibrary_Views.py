from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from api.models import *
from django.contrib import messages
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
def Home(request):
    return render(request,'Laibrary/Home.html')

def AddBook(request):
    if request.method=='POST':
        book_name=request.POST.get('book_name')
        author_name=request.POST.get('author_name')
        publisher_name=request.POST.get('publisher_name')
        available_copies=request.POST.get('available_copies')
        copies=request.POST.get('copies')
        book=Books(
            book_name=book_name,
            author_name=author_name,
            publisher_name=publisher_name,
            copies=copies,
            available_copies=available_copies
        )
        book.save()
        messages.success(request,'Book addedd Successfully')
        return redirect('addbook')
    return render(request,'Laibrary/BookAdd.html')

def SearchBook(request):
    if request.method=='POST':
        book_name=request.POST.get('book_name')
        author_name=request.POST.get('author_name')
        books=Books.objects.filter(book_name__icontains=book_name)
       
       
        context={
           
            'books':books
        }
        return render(request,'Laibrary/BookViews.html',context)
    return render(request,'Laibrary/BookSearch.html')


def IssueBook(request, id):
    book = Books.objects.get(pk=id)
    issue_date = datetime.now().date()
    return_date =issue_date + timedelta(days=5)
    if request.method=='POST':
        # std_name=request.POST.get('std_name')
        std_cnic1=request.POST.get('std_cnic_part1')
        std_cnic2=request.POST.get('std_cnic_part2')
        std_cnic3=request.POST.get('std_cnic_part3')
        student = get_object_or_404(Student,cnic=std_cnic1+'-'+std_cnic2+'-'+std_cnic3)
        # std_roll_no=request.POST.get('std_roll_no')
        book.available_copies -= 1
        book.save()
        try:
            book_instance = Books.objects.get(pk=id)
        except Books.DoesNotExist:
            messages.error(request, 'Invalid Book ID')
            return redirect('searchbook')
        book_issue=Laibrary(
            student_id=student,
            book=book_instance,
            date_of_issue=issue_date,
            date_of_return=return_date

        )
        book=Books(

        )
        book_issue.save()
        messages.success(request,'Book Issued Successfully to Student')
        return redirect('searchbook')
    
    context = {
        'book': book,
        'issue_date': issue_date,
        'return_date': return_date,
    }

    return render(request, 'Laibrary/BookIssue.html', context)

def ReturnBook(request):
    if request.method == 'POST':
        std_cnic1 = request.POST.get('std_cnic_part1')
        std_cnic2 = request.POST.get('std_cnic_part2')
        std_cnic3 = request.POST.get('std_cnic_part3')
        
        student = get_object_or_404(Student, cnic=std_cnic1 + '-' + std_cnic2 + '-' + std_cnic3)
        searches = Laibrary.objects.filter(student_id=student)

        for search in searches:
            if datetime.now().date() > search.date_of_return:
                days_overdues = (datetime.now().date() - search.date_of_return).days
                due_date_fine = days_overdues * 100
                # Update the fine field of the existing Laibrary object and save it
                search.fine = due_date_fine
                search.save()

        context = {
            'searches': searches,
            'student': student,
        }
        return render(request, 'Laibrary/BookReturnView.html', context)

    return render(request, 'Laibrary/BookRetrun.html')

def FineCleared(request, id):
    # Retrieve the Laibrary object with the given id
    student = get_object_or_404(Laibrary, id=id)
    if request.method=='POST':
        student.delete()
        messages.success(request,'Fine Cleared Successfully')
        return redirect('returnbook')
    context = {
        'student': student
    }
    return render(request, 'Laibrary/BookFineCleared.html', context)