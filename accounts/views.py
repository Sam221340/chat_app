from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login, get_user_model
from django.contrib.auth.models import User


# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        c_password = request.POST['c_password']

        if User.objects.filter(username= username):
            messages.error(request, "Username already exist")
            return redirect('signup')

        if User.objects.filter(email= email):
            messages.error(request,'Email already exists')
            return redirect('signup')

        if password != c_password:
            messages.error(request, "Passwords does not match")
            return redirect('signup')

        new_user = User.objects.create_user(username,email,password)
        new_user.save()
        messages.success(request, "USer created successfully")
        return redirect('homepage')
    return render(request,'signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password = password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('chat_home')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'login.html')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('homepage')