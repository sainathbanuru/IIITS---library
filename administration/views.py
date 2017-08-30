# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.base import TemplateView


# Create your views here.

class index(TemplateView):

	template_name = 'administration/index.html'
	context = {}


	def get(self, request, *args, **kwargs):

		return render(request, self.template_name, self.context)
