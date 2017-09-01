from django.forms import Form, CharField, FileField, TextInput, PasswordInput, FileInput, ChoiceField, Select, \
    IntegerField, EmailField
from django.contrib.auth.forms import *
from student.choices import *
from student.models import *

class Book_issue_form(forms.Form):

    # student_roll
    # book_title - choice field
    # book_copies - on selection of title (js)
        # choicefiled with details like available, taken.
        # If taken - estimated return date


    def __init__(self, *args, **kwargs):

        super(Book_issue_formook_issue_form, self).__init__(*args, **kwargs)

        titles = []
        title_list = set(tuple( [ i.title for i in book.objects.all() ] ))

        for i in title_list:
            titles.append((i, i))

        self.fields['titles'].choices = titles

    student_rollno = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'rollno'}))
    book_title = ChoiceField(choices=(), widget=Select(attrs={'class': 'form-control', 'id': 'title'}))
    book_copy = ChoiceField(choices=(), widget=Select(attrs={'class': 'form-control', 'id': 'copy'}))


class add_book_form(forms.Form):

    title = CharField(widget=TextInput(attrs={'class' : 'form-control col-md-7 col-xs-12','id':'title'}))
    author = CharField(widget=TextInput(attrs={'class' : 'form-control col-md-7 col-xs-12','id':'author'}))
    accn = CharField(widget=TextInput(attrs={'class' : 'form-control col-md-7 col-xs-12','id':'accn'}))
    isbn = CharField(widget=TextInput(attrs={'class' : 'form-control col-md-7 col-xs-12','id':'isbn'}))

    #number_of_copies
    noc = IntegerField(widget=TextInput(attrs={'class' : 'form-control','id':'noc'}), initial=1)


class bookDetailsAccn(forms.Form):
    accn = CharField(widget=TextInput(attrs={'class' : 'form-control','id':'accn'}))
