# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class book(models.Model):

    title = models.CharField(max_length=80)
    author = models.CharField(max_length=80)
    accn = models.CharField(max_length=80)
    isbn = models.CharField(max_length=80)

    # Possibilities: shelf, taken, missing
    status = models.CharField(max_length=80, default="shelf")

    def __str__(self):
        return self.title + " - " +  self.author + " : " + self.accn


class issue(models.Model):

    student_rollno = models.CharField(max_length=80)
    book_accn = models.IntegerField(blank=False)

    issue_date_time = models.DateTimeField(default=timezone.now, null=True)
    intended_return_date_time = models.DateTimeField(default=timezone.now, null=True)
    return_date_time = models.DateTimeField(null=True)

    # Possibilities: student, library
    status = models.CharField(max_length=10, default="student")
    fine = models.IntegerField(default=0)

    def __str__(self):
        return str( self.student_rollno ) + " - " + str( self.book_accn )