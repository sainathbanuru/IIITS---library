# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from django.views.generic.base import TemplateView
from .forms import  *
from .models import *
from student.models import *
# Create your views here.

class index(TemplateView):

	template_name = 'administration/index.html'
	context = {}


	def get(self, request, *args, **kwargs):

		return render(request, self.template_name, self.context)


class issue(TemplateView):

	template_name = 'administration/issue.html'
	context = {}

	def get(self, request, *args, **kwargs):
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


        author = str(request.POST['author'])
        title = str(request.POST['title'])
        noc = int(request.POST['noc'])
        accn = list(set(str(request.POST['accn']).split()))
        isbn = str(request.POST['isbn'])

        self.context = {}
        form_class = add_book_form
        form = form_class(None)
        self.context['form'] = form

        if (noc <= 0):
            self.context["error_message"] = "Number of copies should be atleast One !!"
            return render(request, self.template_name, self.context)

        if (len(bookDetails.objects.filter(author=author, title=title)) > 0):
            self.context["error_message"] = 'Book already exists !!  Try updating number of copies !!'
            return render(request, self.template_name, self.context)

        for i in accn:
            if (len(bookDetails.objects.filter(accn = i)) > 0):
                self.context["error_message"] = 'Book with Accn. No ' + i + " already exists !!"
                return render(request, self.template_name, self.context)


        if (len(accn) != noc):
            self.context["error_message"] = "Number of copies and Accn. No didn\'t match !!"
            return render(request, self.template_name, self.context)


        else:

            for i in range(noc):
                b = bookDetails()
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

        self.context['books'] = bookDetails.objects.all()

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
        book = bookDetails.objects.get(accn = accn)
        form_class = bookDetailsAccn
        form = form_class(None)
        self.context['form'] = form
        bookForm = add_book_form
        formBook = add_book_form(initial={'title' : book.title, 'author' : book.author, 'isbn' : book.isbn, 'accn' : book.accn})
        self.context['bookForm'] =  formBook
        self.context['bookDetails'] = book
        self.context['accn'] = accn
        return render(request,self.template_name, self.context)




def bookDetailsUpdate(request,accn):
    context = {}
    template_name = 'administration/bookUpdate.html'
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        isbn = request.POST['isbn']
        accnNo = request.POST['accn']

        if (len(bookDetails.objects.filter(accn=accnNo)) > 0):
            #return HttpResponse("wrong")
            form_class = add_book_form
            book_details_form = bookDetailsAccn
            book = bookDetails.objects.get(accn=accn)
            context['form'] = form_class(None)
            context['bookForm'] = add_book_form(initial={'title' : book.title, 'author' : book.author, 'isbn' : book.isbn, 'accn' : book.accn})
            #context['bookDetails'] = 1
            context['error_message'] = 'Book with Accn. No ' + accnNo + " already exists !!"
            return render(request,template_name,context)

        else:
            b = bookDetails.objects.filter(accn = accn)[0]
            b.title = title
            b.author = author
            b.isbn = isbn
            b.accn = accnNo
            b.save()

            return HttpResponse("saved")


'''
class bookDetailsUpdate(TemplateView):

    template_name = "administration/bookUpdate.html"
    context = {}

    def get(self, request, *args, **kwargs):
        return


    def post(self, request, *args, **kwargs):
        title = request.POST['title']
        author = request.POST['author']
        isbn = request.POST['isbn']
        accn = request.POST['accn']

        if (len(bookDetails.objects.filter(accn = accn)) > 0 ):
            self.context["error_message"] = 'Book with Accn. No ' + i + " already exists !!"
            return render(request, self.template_name, self.context)


'''