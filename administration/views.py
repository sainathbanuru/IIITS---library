# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
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
        return render(request, self.template_name, self.context)

