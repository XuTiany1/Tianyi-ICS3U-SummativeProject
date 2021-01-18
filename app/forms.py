from django import forms

# Import ModelForm 
from django.forms import ModelForm

# Import the models in order to create the form
from app.models import Course, Student, Attendance, Course_Student

# This is the CourseForm, it uses modelform in order to combine models and forms together
class CourseForm(forms.ModelForm):
    # Gets the all the fields in the model to the course form
    class Meta:
        model = Course       
        fields = "__all__"      

#
# To avoid being repetitive, the same goes for StudentForm, AttendanceForm, and CourseStudentForm
#
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"      

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = "__all__" 

class CourseStudentForm(forms.ModelForm):
    class Meta:
        model = Course_Student
        fields = "__all__"

# This is the CourseChoiceField
class CourseChoiceField(forms.Form):
    # Uses the ModelChoiceField which will convert all the courses into a name list
    courses = forms.ModelChoiceField(
        queryset=Course.objects.values_list("name", flat=True).distinct(),
        empty_label=None
    )

#
# The same goes for StudentChoiceField except that it is a list filled with student names instead of course
#
class StudentChoiceField(forms.Form):

    students = forms.ModelChoiceField(
        queryset=Student.objects.values_list("name", flat=True).distinct(),
        empty_label=None
    )                                   