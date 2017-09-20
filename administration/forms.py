from django.forms import Form, CharField, FileField, TextInput, PasswordInput, FileInput, ChoiceField, Select, \
    IntegerField, EmailField, HiddenInput
from django.contrib.auth.forms import *
from student.choices import *
from student.models import *

class Book_issue_form(forms.Form):

    student_rollno = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'rollno'}))
    accn = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'accn','style':'z-index:100'}))
    no_of_days = ChoiceField(choices=days, widget=Select(attrs={'class' : 'form-control','id':'nod'}))



class Book_issue_form2(forms.Form):

    student_rollno = CharField(widget=TextInput(attrs={'readonly':'readonly','class' : 'form-control','id':'rollno'}))

    title = CharField(widget=TextInput(attrs={'readonly':'readonly','class' : 'form-control col-md-7 col-xs-12','id':'title'}))
    author = CharField(widget=TextInput(attrs={'readonly':'readonly','class' : 'form-control col-md-7 col-xs-12','id':'author'}))

    isbn = CharField(widget=TextInput(attrs={'readonly':'readonly','class' : 'form-control col-md-7 col-xs-12','id':'isbn'}))
    accn = CharField(widget=TextInput(attrs={'readonly':'readonly','class' : 'form-control','id':'accn'}))
    no_of_days = CharField(widget=TextInput(attrs={'readonly':'readonly','class' : 'form-control','id':'nod'}))



class Book_return_form(forms.Form):

    student_rollno = CharField(widget=TextInput(attrs={'readonly':'readonly','class' : 'form-control','id':'rollno'}))

    title = CharField(widget=TextInput(attrs={'readonly':'readonly','class' : 'form-control col-md-7 col-xs-12','id':'title'}))
    author = CharField(widget=TextInput(attrs={'readonly':'readonly','class' : 'form-control col-md-7 col-xs-12','id':'author'}))

    isbn = CharField(widget=TextInput(attrs={'readonly':'readonly','class' : 'form-control col-md-7 col-xs-12','id':'isbn'}))
    accn = CharField(widget=TextInput(attrs={'readonly':'readonly','class' : 'form-control','id':'accn'}))

    issue_date = CharField(widget=TextInput(attrs={'readonly':'readonly','class' : 'form-control','id':'issue_date'}))
    intended_return_date = CharField(widget=TextInput(attrs={'readonly':'readonly','class' : 'form-control','id':'intended_return_date'}))

    fine = CharField(widget=TextInput(attrs={'readonly':'readonly','class' : 'form-control','id':'fine'}))




class add_book_form(forms.Form):

    title = CharField(widget=TextInput(attrs={'class' : 'form-control col-md-7 col-xs-12','id':'title'}))
    author = CharField(widget=TextInput(attrs={'class' : 'form-control col-md-7 col-xs-12','id':'author'}))
    accn = CharField(widget=TextInput(attrs={'class' : 'form-control col-md-7 col-xs-12','id':'accn'}))
    isbn = CharField(widget=TextInput(attrs={'class' : 'form-control col-md-7 col-xs-12','id':'isbn'}))
    noc = IntegerField(widget=TextInput(attrs={'class' : 'form-control','id':'noc'}), initial=1)




class Book_update_form(forms.Form):

    title = CharField(widget=TextInput(attrs={'class' : 'form-control col-md-7 col-xs-12','id':'title'}))
    author = CharField(widget=TextInput(attrs={'class' : 'form-control col-md-7 col-xs-12','id':'author'}))
    isbn = CharField(widget=TextInput(attrs={'class' : 'form-control col-md-7 col-xs-12','id':'isbn'}))

    accn = CharField(widget=TextInput(attrs={'class': 'form-control col-md-7 col-xs-12','id':'accn'}))
    prev_accn = CharField(widget=HiddenInput(attrs={'class': 'form-control col-md-7 col-xs-12','id':'prev_accn'}))





class bookDetailsAccn(forms.Form):
    accn = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'accn'}))