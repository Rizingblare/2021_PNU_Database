from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *

# Create your views here.
def index(request):
    studentAll = Students.objects.all()
    studentData = {'studentAll':studentAll}
    return render(request,'StudentManagementSystem/index.html',studentData)

def create(request):
    return render(request,'StudentManagementSystem/add.html')

def edit(request):
    targetID = request.POST['editID']
    editStu = Students.objects.get(id = targetID)
    studentData = {'editStu':editStu}
    return render(request, 'StudentManagementSystem/edit.html', studentData)

def delete(request):
    targetID = request.POST['deleteID']
    deleteID = Students.objects.get(id = targetID)
    deleteID.delete()
    return HttpResponseRedirect(reverse('index'))

def createTodo(request):
    addID = request.POST['addID']
    addFirstName = request.POST['addFirstName']
    addSecondName = request.POST['addSecondName']
    addAge = request.POST['addAge']
    addMajor = request.POST['addMajor']
    addAddress = request.POST['addAddress']
    new_Student = Students(id=addID,firstname=addFirstName,secondname=addSecondName,age=addAge,major=addMajor,address=addAddress)
    new_Student.save()
    return HttpResponseRedirect(reverse('index'))

def editTodo(request):
    targetID = request.POST['editID']
    editStu = Students.objects.get(id=targetID)

    editFirstName = request.POST['editFirstName']
    editSecondName = request.POST['editSecondName']
    editAge = request.POST['editAge']
    editMajor = request.POST['editMajor']
    editAddress = request.POST['editAddress']

    editStu.firstname = editFirstName
    editStu.secondname = editSecondName
    editStu.age = editAge
    editStu.major = editMajor
    editStu.address = editAddress

    editStu.save()
    return HttpResponseRedirect(reverse('index'))