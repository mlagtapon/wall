from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    context = {
        'messages': Message.objects.all().order_by('-created_at'),
        'comments': Comment.objects.all().order_by('created_at')
    }
    return render(request, 'index.html', context)

def wall(request):
    context = {
        'user': User.objects.get(id= request.session['user_id']),
        'messages': Message.objects.all().order_by('-created_at'),
        'comments': Comment.objects.all().order_by('created_at')
    }

    return render(request, 'wall.html', context)

def login(request):
    return render(request, 'login.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        print(errors)
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect('/login')

    else:
        tohash = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        tohashtwo = bcrypt.hashpw(request.POST['confirm'].encode(),bcrypt.gensalt()).decode()
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=tohash, confirm=tohashtwo)

        request.session['first_name'] = user.first_name
        request.session['user_id'] = user.id
        return redirect('/wall')

def loginpage(request):

    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/login')
	
        user = User.objects.filter(email=request.POST['email_login'])
        if len(user) == 0:
            messages.error(request, "Invalid Email/Password.", extra_tags ="login")
            return redirect ('/login')

        if not bcrypt.checkpw(request.POST['password_login'].encode(),user[0].password.encode()):
            messages.error(request, "Invalid Email/Password.", extra_tags ="login")
            return redirect ('/login')
            
        user_id = user[0].id
        request.session['user_id'] = user_id
        return redirect ('/wall')
        
    else: 
        return redirect('/')

def createpost(request):
    
    user_id = request.session['user_id']
    this_user = User.objects.get(id=user_id)

    Message.objects.create(message = request.POST['addmessage'], user=this_user )

    return redirect('/wall')

def createcomment(request):
    
    user_id = request.POST['user_id']
    print(user_id)
    this_user = User.objects.get(id=user_id)

    message_id = request.POST['message_id']
    this_message = Message.objects.get(id=message_id)

    Comment.objects.create(comment = request.POST['addcomment'], user=this_user, message=this_message)

    return redirect('/wall')

def logout(request):

    request.session.clear()

    return redirect('/')
