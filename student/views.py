# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail,BadHeaderError
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.forms.models import model_to_dict
from .models import *
from administration.models import *
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth import authenticate, logout
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from .forms import *
from django.contrib.auth.models import User, Group
from django.template.defaulttags import register
from datetime import date
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django_auth_ldap.config import LDAPSearch, NestedActiveDirectoryGroupType, LDAPGroupType
from django_auth_ldap import backend
from django.conf import settings
import ldap
import time


# Create your views here.
class index(TemplateView):

	template_name = 'student/index.html'
	context = {}


	def get(self, request, *args, **kwargs):

		return render(request, self.template_name, self.context)



################# Function Used for displaying login form and logging users in ##################

class login_user(TemplateView):

	template_name = 'student/login.html'

	def get(self, request, *args, **kwargs):
		context = {}
		return render(request, self.template_name, context)



	def post(self, request, *args, **kwargs):
		context = {}
		print "\n\n\n\n\n\n\nFFFFFFFFFF\n\n\n"

		if "?next" in request.POST:
			return HttpResponse(request.POST['next'])

		username = request.POST['email']
		password = request.POST['pass']

		print "\n\n\n\n\n\n\nFFFFFFFFFF\n\n\n"

		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')

		ldap_backend = backend.LDAPBackend()
		ldap_user = backend.LDAPBackend.authenticate(ldap_backend, username=username, password=password)

		if ldap_user is not None:
			if ldap_user.is_active:
				print "s"
				roll_num = backend.LDAPBackend.populate_user(ldap_backend, username).ldap_user.attrs['gecos'][0]
				roll_no = ''.join([i for i in roll_no if i in "0123456789"])

				# print(str(ldap_user)+" is authenticated")

				AUTH_LDAP_USER_SEARCH = LDAPSearch("OU=prof,OU=people,DC=iiits,DC=in",
												   ldap.SCOPE_SUBTREE, "(uid=%(ldap_user)s)")

				directory = backend.LDAPBackend.populate_user(ldap_backend, username).ldap_user.attrs['homedirectory'][
					0]
				#print directory

				path = directory.split('/')

				#print path
				if "next" in request.POST:
					return HttpResponse(request.POST['next'])

				if str(path[2]) == "students":
					login(request, ldap_user)
					return HttpResponseRedirect('/')



			else:

				context["error_message"] = 'Your account has been disabled'
				return render(request, self.template_name, context)


		else:
			print "no"
			context["error_message"] = 'Invalid login credentials'
			return render(request, self.template_name, context)

		return render(request, self.template_name, context)



def logout_user(request):

    logout(request)
    return HttpResponseRedirect('/login')

