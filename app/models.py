# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# This is the Student model
class Student(models.Model):

    # The name variable for the student, a max length of 100 characters
    name = models.CharField(max_length=100)
    # The contact information for the student phone. Max Length of 100 characters
    phone = models.CharField(max_length=100)
    # The ocntact information for the student email. Max lenggth of 100 characters
    email = models.EmailField(max_length=100)

    # A to-string method which returns the string representation of Student name
    def __str__(self):
        return self.name
    # Make sure that student are unique and the teacher cannot create repetitive entries 
    class Meta: 
        unique_together = ['name', 'phone','email']

# This is the Class model
class Course(models.Model):

    # The name varaible for the class, a max length of 100 characters
    name = models.CharField(max_length=100)
    # The period variable for the class, a max length of 100 characters
    period = models.CharField(max_length=100)
    # The place variable for the class, a max length of 100 characters
    place = models.CharField(max_length=100) 
    # The price varaible for the class, the default price for a class set to 0 and cannot be less than 0
    price = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    # The start date for the class
    start = models.DateField()
    # The end date for the class
    end = models.DateField()

    # A to-string method which returns the string representation of the class name
    def __str__(self):
        return self.name
    # Make sure that courses are unique and the teacher cannot create repetitive entries 
    class Meta: 
        unique_together = ['name', 'period','place']


# This is the Attendance model
class Attendance(models.Model):
    # Defines the foreignKey of the course
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # Defines the foreignKey of the student
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    # Defines the date that the attendance occurs
    date_attended = models.DateField()

# This is the many-to-many model that links student and class for registration
class Course_Student(models.Model):
    # Defines the foreignKey of the course
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # Defines the foreidnKey of the student
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    # Defines the amount of times student attended, initially set to 0 and cannot be negative
    attend_times = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    # Defines the total amount of paid_credit, initially set to 0 and cannot negative
    paid_credit = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    # Defines the student's current balance, initially set to 0
    balance = models.IntegerField(default=0)
    # Defines the student's latest test score
    score = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    # Makes sure that course and student are unique pairs to avoid repetition
    class Meta:
        unique_together = ['course', 'student']
