from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Task
from django.contrib.auth.decorators import login_required
from datetime import datetime
# Create your views here.

def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        
        user = User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('login')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid Credentials !")
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def task_create_view(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        if deadline:
            deadline = datetime.strptime(deadline, "%Y-%m-%d").date()

        task = Task.objects.create(
            user = request.user,
            title = title,
            description=description,
            deadline=deadline
        )
        return redirect('dashboard') # task_list
    return render(request, 'create_task.html')

@login_required
def task_list_view(request):
    tasklist = Task.objects.filter(user=request.user)
    return render(request, 'list_of_task.html',{'tasklist':tasklist})

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


@login_required
def update_view(request, id):
    tsk = Task.objects.get(id=id, user=request.user)
    if request.method == "POST":
        tsk.title = request.POST.get('title')
        tsk.description = request.POST.get('description')
        tsk.deadline=request.POST.get('deadline')
        if tsk.deadline:
            tsk.deadline = datetime.strptime(tsk.deadline, "%Y-%m-%d").date()
        tsk.status=request.POST.get('status')
        tsk.save()
        return redirect("list_of_task")
    return render(request, 'update.html', {"tsk": tsk})

@login_required
def delete_view(request, id):
    task = Task.objects.get(id=id, user=request.user)
    task.delete()
    return redirect('list_of_task')