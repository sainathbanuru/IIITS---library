# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.utils import timezone
from student.models import *
from .forms import  *
from .models import *

import datetime
import json
import re


# Create your views here.

class index(TemplateView):

	template_name = 'administration/index.html'
	context = {}


	def get(self, request, *args, **kwargs):
            books = len(book.objects.all().values_list("title",flat=True).distinct())
            self.context['books'] = books
            self.context['bookIssues'] = len(issue.objects.all())
            return render(request, self.template_name, self.context)




class issue_book(TemplateView):

    template_name = 'administration/issue.html'
    context = {}

    def get(self, request, *args, **kwargs):
        
        self.context = {}

        form_class = Book_issue_form
        form = form_class(None)
        self.context['form'] = form

        return render(request, self.template_name, self.context)


    def post(self, request, *args, **kwargs):

        self.context = {}

        roll_no = str( request.POST['student_rollno'] ).upper()
        accn = int( request.POST['accn'] )
        nod = int( request.POST['no_of_days'] )



        # Implies it's second post not the first .....
        try:
                
            title = str( request.POST['title'] )


            # Checking for refresh
            b = book.objects.get(accn=accn)

            # Means book isn't there in the shelf
            if b.status != "shelf":
                self.context['form'] = Book_issue_form
                self.context['error_message'] = "Book with given accn number '" + str(accn) + "' isn't available in the library currently !!"
                return render(request, self.template_name, self.context)    




            # Issueing starts ....
            book_issue = issue()
            
            book.objects.filter(accn = accn).update( status = "taken" )

            book_issue.student_rollno = str(roll_no)
            book_issue.book_accn = accn
            book_issue.issue_date_time = datetime.datetime.now()
            book_issue.intended_return_date_time = datetime.datetime.now() + datetime.timedelta(days = nod)
            book_issue.status = "student"
            
            book_issue.save()


            self.context["success"] = True
            self.context["form"] = Book_issue_form
            return render(request, self.template_name, self.context)



        # Implies POST got only roll, accn => First POST submit ...
        except:
   
            pattern = re.compile("^201[0-9]{6}$")
            self.context['form'] = Book_issue_form(initial={'student_rollno': roll_no, 'accn': accn})


            if roll_no[0] == "I" and roll_no[1] == "S":
                roll_no = roll_no[2:]


            # Implies roll number is mostly invalid
            if not pattern.match(roll_no):
                self.context["error_message"] = "Check the Roll number you entered !!"
                return render(request, self.template_name, self.context)    
            


            try:

                b = book.objects.get(accn=accn)

                # Means book isn't there in the shelf
                if b.status != "shelf":
                    self.context['error_message'] = "Book with given accn number isn't available in the library currently !!"
                    return render(request, self.template_name, self.context)    


                # Book is there in lib
                else:
                    self.context['isbn'] = b.isbn
                    self.context['second_time'] = True
                    self.context['form'] = Book_issue_form2(initial={'student_rollno': roll_no, 'title' : b.title, 'author' : b.author, 'isbn' : b.isbn, 'accn' : b.accn, 'no_of_days': nod})

                    return render(request, self.template_name, self.context)

            except:

                self.context['error_message'] = "Book doesn't exist with given accn"
                return render(request, self.template_name, self.context)
                


def student_has_book(roll_no, accn):

    issues_list = issue.objects.filter(student_rollno=roll_no, book_accn=accn)

    if len(issues_list) == 0:
        return False

    else:

        for i in issues_list:
            if i.status == "student":
                return True

        return False



class book_return(TemplateView):

    template_name = 'administration/book_return.html'
    context = {}

    def get(self, request, *args, **kwargs):
        
        self.context = {}
        
        form_class = Book_issue_form
        form = form_class(None)
        self.context['form'] = form
        
        return render(request, self.template_name, self.context)


    def post(self, request, *args, **kwargs):

        self.context = {}
        accn = int( request.POST['accn'] )


        # Implies it's second post not the first .....
        try:
            
            title = str( request.POST['title'] )

            b = book.objects.get(accn=accn)

            if b.status == "shelf":
                self.context['form'] = Book_issue_form(None)
                self.context['error_message'] = "Book with given accn number '" + str(accn) + "' is in the library currently !!"
                return render(request, self.template_name, self.context)    

            

            issue.objects.filter(book_accn=accn, status="student").update( return_date_time=datetime.datetime.now(), status="library")
            book.objects.filter(accn = accn).update( status = "shelf" )

            self.context["success"] = True
            self.context['form'] = Book_issue_form(None)
            return render(request, self.template_name, self.context)    





        # Implies POST got only roll, accn => First POST submit ...
        except:

            self.context['form'] = Book_issue_form(initial={'accn': accn})

            try:

                b = book.objects.get(accn=accn)

                # Means book isn't there in the shelf
                if b.status == "shelf":
                    self.context['error_message'] = "Book with given accn number is in the library currently !!"
                    return render(request, self.template_name, self.context)    


                # Book is not there in lib
                else:

                    iss = issue.objects.get( book_accn=accn, status="student" )
                    
                    self.context['isbn'] = b.isbn
                    self.context['second_time'] = True

                    if int(( timezone.now() - iss.intended_return_date_time ).days) > 0:
                        self.context['days_delayed'] = str( int( ( timezone.now() - iss.intended_return_date_time ).days ) )



                    # issue_date, intended_return_date
                    i_d = str( iss.issue_date_time.day ) + "/" + str( iss.issue_date_time.month ) + "/" + str( iss.issue_date_time.year )
                    i_r_d = str( iss.intended_return_date_time.day ) + "/" + str( iss.intended_return_date_time.month ) + "/" + str( iss.intended_return_date_time.year )


                    self.context['form'] = Book_return_form(initial={'student_rollno': iss.student_rollno, 'title' : b.title, 'author' : b.author, 'accn' : b.accn, 'issue_date': i_d, 'intended_return_date': i_r_d})

                    return render(request, self.template_name, self.context)


            except:
                self.context['error_message'] = "Book doesn't exist with given accn"
                return render(request, self.template_name, self.context)
                



class add_book(TemplateView):

    template_name = "administration/add_book.html"
    context = {}

    def get(self, request, *args, **kwargs):
      
        self.context = {}
      
        form_class = add_book_form
        form = form_class(None)
        self.context['form'] = form

        return render(request, self.template_name, self.context)


    def post(self, request, *args, **kwargs):


        title = str(request.POST['title'])
        author = str(request.POST['author'])
        isbn = str(request.POST['isbn'])
        noc = int(request.POST['noc'])
        accn = list(set( str(request.POST['accn']).split() ))
        

        self.context = {}
        self.context['form'] = add_book_form(initial={'title': title, 'author': author, 'isbn': isbn, 'noc': noc, 'accn': accn})



        # Possible error scenarios
        if (noc <= 0):
            self.context["error_message"] = "Number of copies should be atleast One !!"
            return render(request, self.template_name, self.context)


        if ( len(book.objects.filter(author=author, title=title)) > 0):
            self.context["error_message"] = 'Book already exists !!  Try updating number of copies !!'
            return render(request, self.template_name, self.context)


        for i in accn:
            if (len(book.objects.filter(accn = i)) > 0):
                self.context["error_message"] = 'Book with Accn. No - ' + i + " already exists !!"
                return render(request, self.template_name, self.context)


        if (len(accn) != noc):
            self.context["error_message"] = "Number of copies and Accn. No didn\'t match !!"
            return render(request, self.template_name, self.context)


        # No errors ...
        for i in range(noc):
            
            b = book()
            
            b.author = author
            b.title = title
            b.accn = accn[i]
            b.isbn = isbn
            
            b.save()


        self.context["success"] = True
        return render(request, self.template_name, self.context)



class bookList(TemplateView):

    template_name = "administration/bookList.html"
    context = {}

    def get(self, request, *args, **kwargs):

        self.context['books'] = book.objects.all()
        return render(request, self.template_name, self.context)




class bookUpdate(TemplateView):

    template_name = "administration/bookUpdate.html"
    context = {}

    def get(self, request, *args, **kwargs):
    
        self.context = {}
    
        form_class = bookDetailsAccn
        form = form_class(None)
        self.context['form'] = form

        return render(request, self.template_name, self.context)


    def post(self, request, *args, **kwargs):
        
        accn = request.POST['accn']
        
        self.context = {}
        self.context['form'] = bookDetailsAccn(initial={'accn': accn})
        

        try:
            
            b = book.objects.get(accn = accn)

            self.context['accn'] = accn
            self.context['isbn'] = b.isbn
            self.context['bookDetails'] = b
            self.context['bookForm'] =  Book_update_form(initial={'title' : b.title, 'author' : b.author, 'isbn' : b.isbn, 'accn' : b.accn, 'prev_accn': b.accn})
            
            return render(request, self.template_name, self.context)

        except:
           
            self.context["error_message"] = "Book doesn't exist with given accn"
            return render(request, self.template_name, self.context)

        

def bookDetailsUpdate(request,accn):
    
    context = {}
    template_name = 'administration/bookUpdate.html'
    

    if request.method == 'POST':
    

        title = request.POST['title']
        author = request.POST['author']
        isbn = request.POST['isbn']
        
        accnNo = request.POST['accn']
        original_accn = request.POST['prev_accn']


        if accnNo != original_accn and ( len(book.objects.filter(accn=accnNo) ) > 0):
            
            b = book.objects.get(accn=accnNo)
    
            context['accn'] = accn
            context['bookDetails'] = b
            context['form'] = bookDetailsAccn(initial={'accn': original_accn})
            context['bookForm'] = Book_update_form(initial={'title' : b.title, 'author' : b.author, 'isbn' : b.isbn, 'accn' : b.accn, 'prev_accn': original_accn})
    
            context['error_message'] = 'Book with Accn. No - ' + str(accnNo) + " already exists !!"
            return render(request,template_name,context)


        else:

            context['form'] = bookDetailsAccn(None)
            context["success"] = True
            book.objects.filter(accn=original_accn).update( title=title, author=author, isbn=isbn, accn=accnNo )

            return render(request, template_name, context)



def autocomplete(request):

    if request.is_ajax():
    
        print 'hello'
    
        queryset = book.objects.filter(title__startswith=request.GET.get('search', None))
        list = []
    
        for i in queryset:
            list.append(i.title)
        data = {
            'list': list,
        }
    
        print data
        return JsonResponse(data)