# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class bookDetails(models.Model):

    title = models.CharField(max_length=80)
    author = models.CharField(max_length=80)
    accn = models.CharField(max_length=80)
    isbn = models.CharField(max_length=80)
    status = models.CharField(max_length=80, default="shelf")

    def __str__(self):
        return self.title + " - " +  self.author
