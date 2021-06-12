from django.shortcuts import render, redirect
from django.contrib import messages 
from .models import User
import bcrypt

# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST ['first_name'],
            last_name = request.POST ['last_name'],
            email = request.POST ['email'],
            password = pw_hash,
        )
        request.session['userid'] = new_user.id 
        return redirect('/dash')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:    
        user = User.objects.filter(email = request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id 
                return redirect('/dash')
            else:
                messages.error(request, 'Invalid password')
            return redirect('/')
        return redirect('/')

def dash(request):
    if 'userid' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    context = {
        'user': user,
    }
    return render(request, 'dash.html', context)

def new_rec(request):
    return render(request, 'newRecipe.html')




def logout(request):
    request.session.clear()
    return redirect('/')

