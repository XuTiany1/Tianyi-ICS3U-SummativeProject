# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.http import HttpResponseRedirect

# Import the models and forms I created to write the views
from .forms import CourseForm, StudentForm,AttendanceForm,CourseStudentForm,CourseChoiceField,StudentChoiceField
from .models import Course, Student,Course_Student,Attendance


@login_required(login_url="/login/")

# Method Name: index
# Method Parameter: request, which is the user's request
# This brings the user to the home screen
def index(request):
    return render(request, "index.html")

# Method Name: updateRegistrationTable
# Method Parameter:
#                 1. course, which is the course the user wishes to update the registration
#                 2. student, which is the student the user wishes to make changes to
# This method takes the selected course and student and update their information in the course and student table
def updateRegistrationTable(course, student):
        # Finds the registration the user performs
        registration = Course_Student.objects.filter(course=course, student=student).first()
        # Finds the amount of times a student attended class
        attendTimes = Attendance.objects.filter(course=course, student=student).count()
        registration.attend_times = attendTimes
        # Update the student's balance
        registration.balance = registration.paid_credit - attendTimes*course.price
        registration.save()

# Method Name: refreshRegistrationTable
# Method Parameter: none
# This method does the same thing as updateRegistrationTable but updates everything on the registration table
def refreshRegistrationTable():
    # Takes all the objects from Course_Student form
    existingRegistrations = Course_Student.objects.all()
    # Loop through all the objets
    for r in existingRegistrations:
        # Update the objects
        updateRegistrationTable(r.course, r.student)

# Method Name: handleDeleteCourse
# Method Parameter: request, which is the user's request
# This method allows the user to delete a course from the courses table in courses.html
def handleDeleteCourse(request):
    
    # 1.Delete the course from databse
    if request.method == 'POST':
        courseName = request.POST.get("targetCourse"," ")
        course = get_object_or_404(Course, pk=courseName)
        course.delete()

    # 2. redirect to courses.html
    return HttpResponseRedirect("/courses.html")    

# Method Name: handleEditCourse
# Method Parameter: request, which is the user's request
# This method allows the user to edit a course from the courses table in courses.html
def handleEditCourse(request):
    
    # 1.Save the course to database
    if request.method == 'POST':
        # retrieves the required information about the course
        coursePk = request.POST.get("targetCourse"," ")
        courseName = request.POST.get("editCourse_name"," ")
        coursePeriod = request.POST.get("editCourse_period"," ")
        coursePlace = request.POST.get("editCourse_place"," ")
        coursePrice = request.POST.get("editCourse_price"," ")
        courseStart = request.POST.get("editCourse_start"," ")
        courseEnd = request.POST.get("editCourse_end"," ")
        
        #update the database
        course = get_object_or_404(Course, pk=coursePk)
        course.name = courseName
        course.period = coursePeriod
        course.price = coursePrice
        course.place = coursePlace
        course.start = courseStart
        course.end = courseEnd
        course.save()

    # 2. redirect to courses.html
    return HttpResponseRedirect("/courses.html")        

# Method Name: handleAddCourse
# Method Parameter: request, which is the user's request
# This method allows the user to add a course to the courses table in courses.html
def handleAddCourse(request):
    
    # 1. Valid the input and Save form to database
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        courseForm = CourseForm(request.POST)

        # check whether it's valid:
        if courseForm.is_valid():
            # process the data in form.cleaned_data as required
            courseForm.save()

    # 2. redirect to courses.html
    return HttpResponseRedirect("/courses.html")

# Method Name: handleCourses
# Method Parameter: request, which is the user's request
# This method allows the user to display the course on the courses table in courses.html
def handleCourses(request):

    # 1. Retrieve all the existing data from Course Table
    existingCourses = Course.objects.all()

    # define the context with the data
    context = {
        'existingCourses': existingCourses,
    }
    # 2. Redirect to courses.html with the data
    return render(request, 'courses.html', context) 

# Method Name: handleDeleteStudent
# Method Parameter: request, which is the user's request
# This method allows the user to delete a student from the students table in students.html
def handleDeleteStudent(request):
    
    # 1.Delete the course from database
    if request.method == 'POST':
        studentName = request.POST.get("targetStudent"," ")
        student = get_object_or_404(Student, pk=studentName)
        student.delete()

    # 2. redirect to students.html
    return HttpResponseRedirect("/students.html")    

# Method Name: handleEditStudent
# Method Parameter: request, which is the user's request
# This method allows the user to edit a student from the students table in students.html
def handleEditStudent(request):
    
    # 1.Retrieve the user input and update database
    if request.method == 'POST':
        studentPk = request.POST.get("targetStudent"," ")
        studentName = request.POST.get("editStudent_name"," ")
        studentPhone = request.POST.get("editStudent_phone"," ")
        studentEmail = request.POST.get("editStudent_email"," ")
        
        #update the database
        student = get_object_or_404(Student, pk=studentPk)
        student.name = studentName
        student.phone = studentPhone
        student.email = studentEmail
        student.save()

    # 2. redirect to students.html
    return HttpResponseRedirect("/students.html")        

# Method Name: handleAddStudent
# Method Parameter: request, which is the user's request
# This method allows the user to add a student from the students table in students.html
def handleAddStudent(request):
    
    # 1. Valid the input and Save form to database
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        studentForm = StudentForm(request.POST)

        # check whether it's valid:
        if studentForm.is_valid():
            # save the data in form.cleaned_data to database
            studentForm.save()

    # 2. redirect to courses.html
    return HttpResponseRedirect("/students.html")

# Method Name: handleStudents
# Method Parameter: request, which is the user's request
# This method allows the user to display the students on the students table in students.html
def handleStudents(request):

    # 1. Retrieve all the existing student data from database
    existingStudents = Student.objects.all()

    # define the context with the data
    context = {
        'existingStudents': existingStudents,
    }
    # 2. Redirect to courses.html with the data
    return render(request, 'students.html', context)

# Method Name: handleDeleteRegistration
# Method Parameter: request, which is the user's request
# This method allows the user to delete a registration on the registration table in registration.html
def handleDeleteRegistration(request):
    
    # 1.Get the user input and delete the selected registration from database
    if request.method == 'POST':
        registrationPk = request.POST.get("targetRegistration"," ")
        registration = get_object_or_404(Course_Student, pk=registrationPk)
        registration.delete()

    # 2. redirect to courses.html
    return HttpResponseRedirect("/registration.html")    

# Method Name: handleEditRegistration
# Method Parameter: request, which is the user's request
# This method allows the user to edit a registration on the registration table in registration.html
def handleEditRegistration(request):
    
    # 1.Retrieve the user input and save the updated registration to database
    if request.method == 'POST':
        registrationPk = request.POST.get("targetRegistraton"," ")
        registrationPaidCredit = request.POST.get("editRegistration_paid_credit"," ")
        registrationScore = request.POST.get("editRegistration_score"," ")
        
        #update the database
        registration = get_object_or_404(Course_Student, pk=registrationPk)
        registration.paid_credit = registrationPaidCredit
        registration.score = registrationScore
        registration.save()

        updateRegistrationTable(registration.course, registration.student)

    # 2. redirect to courses.html
    return HttpResponseRedirect("/registration.html")  

# Method Name: handleAddRegistration
# Method Parameter: request, which is the user's request
# This method allows the user to add a registration on the registration table
def handleAddRegistration(request):
    
    # 1. Valid the input and Save form to database
    if request.method == 'POST':
        # Retrieve the user input about: the student name, the course name, and the student's current credit
        studentName = request.POST.get("students"," ")
        courseName = request.POST.get("courses"," ")
        paidCredit = request.POST.get("paid_credit"," ")

        # If the studentName or courseName is empty, then an error message will be displayed
        if (studentName == " " or courseName == " "):
            html_template = loader.get_template( 'error-400.html' )
            context = {
                "errorMessage" : "Please select a course and a student"
            }
            return HttpResponse(html_template.render(context, request))    

        # Find the student's entry in its table
        selectedStudent = Student.objects.filter(name=studentName).first()
        # Find the course's entry in its table
        selectedCourse = Course.objects.filter(name=courseName).first()

        # Create another entry in the Course_Student form
        registration = Course_Student(
            course=selectedCourse,
            student=selectedStudent,
            paid_credit=paidCredit
        )

        # try-except loop to try to register the student with its course
        try:
            registration.save()
        # if it ere already exists a registration of the student and course, then an error message will be displayed
        except Exception:
            html_template = loader.get_template( 'error-400.html' )
            context = {
                "errorMessage" : "The student already registers the course "
            }
            return HttpResponse(html_template.render(context, request))    

        # redirect to registration.html
        return HttpResponseRedirect("registration.html")

    # Send the list of courses and students data to the registration page
    courseList = CourseChoiceField()
    studentList = StudentChoiceField()

    context = {
        'courseList':courseList,
        'studentList':studentList,
    }
       
    return render(request, 'register.html', context)

# Method Name: handleRegistration
# Method Parameter: request, which is the user's request
# This method helps display the registration information
def handleRegistration(request):
    # Update all the students on the registration table
    refreshRegistrationTable()
    # Gets all the many-to-many relationship between the course and student 
    existingRegistrations = Course_Student.objects.all()

    context = {
        'existingRegistrations': existingRegistrations,
    }
    # Return the relationships information to help display the registration
    return render(request, 'registration.html', context)   

# Method Name: handleDeleteAttendance
# Method Parameter: request, which is the user's request
# This method allows the user to delete an attendance on the attendance table in attendance.html
def handleDeleteAttendance(request):
    
    # 1.Delete the attendance from database
    if request.method == 'POST':
        # Get the primary key of the targetAttendance 
        attendancePk = request.POST.get("targetAttendance"," ")
        attendance = get_object_or_404(Attendance, pk=attendancePk)
        course = attendance.course
        student = attendance.student
        # Delete attendance
        attendance.delete()
        # Update the student's credit 
        updateRegistrationTable(course, student)

    # 2. redirect to attendance.html
    return HttpResponseRedirect("/attendance.html") 

# Method Name: handleEditAttendance
# Method Parameter: request, which is the user's request
# This method allows the user to edit an attendance on the attendance table in attendance.html
def handleEditAttendance(request):
    
    # 1.Retrive the user input and save the updated attendance info to database
    if request.method == 'POST':
        # Get the primary key of the targetAttendance
        attendancePk = request.POST.get("targetAttendance"," ")
        attendanceDate = request.POST.get("editAttendance_date_attended"," ")
        
        #update the databse
        attendance = get_object_or_404(Attendance, pk=attendancePk)
        attendance.date_attended = attendanceDate
        attendance.save()

    # 2. redirect to courses.html
    return HttpResponseRedirect("/attendance.html")  

# Method Name: handleAddAttendanceSelectCourse
# Method Parameter: request, which is the user's request
# This allows the user to select a course when they are trying to do their attendance
def handleAddAttendanceSelectCourse(request):
    
    # Retreive the user input and select the course 
    if request.method == 'POST':
        # Get the user's choice for course
        courseName = request.POST.get("courses"," ")
        # Based on the courseName find the course in the Course form
        selectedCourse = Course.objects.filter(name=courseName).first()
        # Retrieve the students who registered to this course
        registration_list = list(Course_Student.objects.filter(course=selectedCourse))
        
        # Display information
        context = {
            "coursename" : courseName,
            "registration_list" : registration_list,
        }

        return render(request, 'attend.html', context)

    # If the request method is not post, then it would be get
    # Display the courselist for the user to choose
    courseList = CourseChoiceField()

    context = {
        'courseList':courseList,
    }
       
    return render(request, 'attend-selectcourse.html', context)

# Method Name: handleAddAttendance
# Method Parameter: request, which is the user's request
# This allows the user to finish adding their attendance
def handleAddAttendance(request):

    #  Valid the input and Save new attedance entry to database
    if request.method == 'POST':
        # Get the user's choice for student
        studentList = request.POST.getlist('attendance_students',"")

        # If there were no student, then the teacher shouldn't be able to submit an attendance sheet
        if (len(studentList) == 0):
            html_template = loader.get_template( 'error-400.html' )
            context = {
                "errorMessage" : "There is currently no student enrolled, please check again"
            }
            return HttpResponse(html_template.render(context, request))   

        # Retrieve the user's target course
        courseName = request.POST.get("target_course"," ")
        # Get the user's choice for date
        date = request.POST.get("attendance_date"," ")
        # Based on courseName, find the course in the courseForm
        selectedCourse = Course.objects.filter(name=courseName).first()

        # Loop through the studentName in the studentList
        for studentName in studentList:
            # Uses the student name to find its corresponding object
            selectedStudent = Student.objects.filter(name=studentName).first()
            # Create a new attendance record
            attendance = Attendance(
                course=selectedCourse,
                student=selectedStudent,
                date_attended=date
            )
            # Save the attendance
            attendance.save()

            # update registration table
            updateRegistrationTable(selectedCourse, selectedStudent)

        # redirect to registration.html
        return HttpResponseRedirect("attendance.html")

    # On the off chance that there is an error and the method is not post, then it will be redirected to index.html
    return render(request, 'index.html')

# Method Name: handleAttendance
# Method Parameter: request, which is the user's request
# This method helps display the attendance sheet
def handleAttendance(request):
    # Gets all the attendance from Attendance table
    existingAttendances = Attendance.objects.all()

    context = {
        'existingAttendances': existingAttendances,
    }
    # Return the data
    return render(request, 'attendance.html', context)             

# Method Name: pages
# Method Parameter: request, which is the user's request
# This method determines which method the user wishes to perform
@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        # The reason for this is because all the templates become unique and identifiable after the / sign
        load_template = request.path.split('/')[-1]

        # The for loops checks what is the html template and performs the corresponding action
        if (load_template == "addCourse.html"):
            return handleAddCourse(request)
       
        if (load_template == "editCourse.html"):
            return handleEditCourse(request)    

        if (load_template == "deleteCourse.html"):
            return handleDeleteCourse(request)
                
        if (load_template == "courses.html"):
            return handleCourses(request)

        if (load_template == "addStudent.html"):
            return handleAddStudent(request)
       
        if (load_template == "editStudent.html"):
            return handleEditStudent(request)    

        if (load_template == "deleteStudent.html"):
            return handleDeleteStudent(request)
                
        if (load_template == "students.html"):
            return handleStudents(request)

        if (load_template == "register.html"):
            return handleAddRegistration(request)

        if (load_template == "editRegistration.html"):
            return handleEditRegistration(request)    

        if (load_template == "deleteRegistration.html"):
            return handleDeleteRegistration(request)
                
        if (load_template == "registration.html"):
            return handleRegistration(request)    
       
        if (load_template == "attend-selectcourse.html"):
            return handleAddAttendanceSelectCourse(request)
        
        if (load_template == "attend.html"):
            return handleAddAttendance(request)

        if (load_template == "editAttendance.html"):
            return handleEditAttendance(request)    

        if (load_template == "deleteAttendance.html"):
            return handleDeleteAttendance(request)
                
        if (load_template == "attendance.html"):
            return handleAttendance(request)                   

        # If the load_template did not equal to any of the above templates, it will be 
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
    
    # If the template does not exist, then error 404 message will be displayed
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'error-404.html' )
        return HttpResponse(html_template.render(context, request))
    # Else, error 500 message will be displayed
    except:
    
        html_template = loader.get_template( 'error-500.html' )
        return HttpResponse(html_template.render(context, request))


