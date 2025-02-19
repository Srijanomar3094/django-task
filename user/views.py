from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignUpForm
from .models import Roles


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            role = Roles.objects.get(user=user).role.field
            if role == 'Patient':
                return redirect('patient_dashboard')
            elif role == 'Doctor':
                return redirect('doctor_dashboard')
        else:
            print("Form errors:", form.errors) 
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            role = Roles.objects.get(user=user).role.field
            if role == 'Patient':
                return redirect('patient_dashboard')
            elif role == 'Doctor':
                return redirect('doctor_dashboard')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})
    return render(request, 'users/login.html')

def patient_dashboard(request):
    user = request.user
    return render(request, 'users/patient_dashboard.html', {'user': user})

def doctor_dashboard(request):
    user = request.user
    return render(request, 'users/doctor_dashboard.html', {'user': user})