from django.shortcuts import render, redirect


def register_view(request):
    return render(request, 'frontend/register.html')


def login_view(request):
    return render(request, 'frontend/login.html')


def dashboard_view(request):
    return render(request, 'frontend/dashboard.html')


def patients_view(request):
    return render(request, 'frontend/patients.html')


def doctors_view(request):
    return render(request, 'frontend/doctors.html')


def mappings_view(request):
    return render(request, 'frontend/mappings.html')


def home_view(request):
    return redirect('login')
