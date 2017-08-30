# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class book(models.Model):

    title = models.CharField(max_length=80)
    author = models.CharField(max_length=80)

    def __str__(self):
        return self.title


class booking(models.Model):

    avaialability = models.BooleanField(default=False)
    student_rollno = models.CharField(max_length=20, blank=True)
    book_id = models.PositiveIntegerField()

    issued = models.BooleanField(default=False)
    issue_date = models.DateField()
    returned_date = models.DateField()
    renewed_date = models.DateField()

    def __str__(self):
        return  self.student_rollno