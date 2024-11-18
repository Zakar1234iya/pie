from django.shortcuts import render, redirect
from .models import User, Pie ,UserManager , PieManager
from django.contrib import messages
from . import models
import bcrypt

# Index View
def index(request):
    return render(request, "index.html")

# Register View
def register(request):
    if request.method == 'POST':
        password = request.POST['password']
        re_password = request.POST['re_password']
        if password != re_password:
            messages.error(request, "Passwords do not match.", extra_tags='register')
            return redirect('/register')
        errors = UserManager.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='register')
            return redirect('/register')
        else:
            User.objects.add_user(request.POST)
            messages.success(request, "Registration successful! You can now log in.", extra_tags='success')
            return redirect('/')
    return render(request, 'index.html')

# Login View
def login(request):
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['id'] = logged_user.id
                return redirect('/dashboard')
            else:
                messages.error(request, "Invalid email or password", extra_tags='login')
        else:
            messages.error(request, "Invalid email or password", extra_tags='login')
        return redirect('/login')
    return render(request, 'index.html')

# Logout View
def logout(request):
    request.session.clear()
    return redirect('/')

# Profile View
def profile(request):
    if 'id' not in request.session:
        messages.error(request, 'You must login first to view this page.', extra_tags='login')
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    pies = Pie.objects.filter(baker=user)
    context = {
        'pies': pies,
        'current_user': user
    }
    return render(request, 'dashboard.html', context)


# Add Pie View
def add_pie(request):
    if 'id' not in request.session:
        messages.error(request, 'You must login first to add a pie.', extra_tags='login')
        return redirect('/')
    if request.method == 'POST':
        errors = Pie.objects.pie_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='failed')
            return redirect('/dashboard')
        else:
            Pie.objects.add_pie(request.POST, request.session['id'])
            messages.success(request, "Pie added.", extra_tags='success')
            return redirect('/dashboard')
    return redirect('/dashboard')

# View All Pies
def view_pie(request):
    if 'id' not in request.session:
        messages.error(request, 'You must login first to view this page.', extra_tags='login')
        return redirect('/')
    context = {
        'pies': Pie.objects.all()
    }
    return render(request, 'pies.html', context)

# View Specific Pie
def view_pies(request, id):
    if 'id' not in request.session:
        messages.error(request, 'You must login first to view this page.', extra_tags='login')
        return redirect('/')
    
    pie = Pie.objects.get(id=id)
    user_voted = False
    
    if 'voted_pies' in request.session and str(id) in request.session['voted_pies']:
        user_voted = True
    
    context = {
        'pie': pie,
        'baker': pie.baker,
        'user_voted': user_voted,
    }
    return render(request, 'show.html', context)


# Edit Pie Page
def edit_pie(request, id):
    if 'id' not in request.session:
        messages.error(request, 'You must login first to edit this page.', extra_tags='login')
        return redirect('/')
    pie = Pie.objects.get(id=id)
    context = {
        'pie': pie
    }
    return render(request, 'edit.html', context)


# Submit Pie Edit
def update_pie(request):
    if 'id' not in request.session:
        messages.error(request, 'You must login first to edit this page.', extra_tags='login')
        return redirect('/')
    if request.method == 'POST':
        pie = Pie.objects.get(id=request.POST['pie_id'])
        pie.piename = request.POST['piename']
        pie.filling = request.POST['filling']
        pie.crust = request.POST['crust']
        pie.save()
        messages.success(request, "Pie updated.", extra_tags='success')
    return redirect('/dashboard')

# Increase Vote
def incvote(request):
    if 'id' not in request.session:
        messages.error(request, 'You must login first to vote.', extra_tags='login')
        return redirect('/')
    
    pie_id = request.POST['pie_id']
    if 'voted_pies' not in request.session:
        request.session['voted_pies'] = []

    if pie_id in request.session['voted_pies']:
        messages.error(request, 'You have already voted for this pie.', extra_tags='voted')
        return redirect('/pies')
    
    pie = Pie.objects.get(id=pie_id)
    pie.vote += 1
    pie.save()
    
    request.session['voted_pies'].append(pie_id)
    request.session.modified = True
    
    messages.success(request, "Your vote has been cast.", extra_tags='success')
    return redirect('/pies')

# Decrease Vote
def decvote(request):
    if 'id' not in request.session:
        messages.error(request, 'You must login first to remove vote.', extra_tags='login')
        return redirect('/')
    
    pie_id = request.POST['pie_id']
    if 'voted_pies' not in request.session:
        request.session['voted_pies'] = []

    if pie_id not in request.session['voted_pies']:
        messages.error(request, 'You have not voted for this pie.', extra_tags='not_voted')
        return redirect('/pies')

    pie = Pie.objects.get(id=pie_id)
    pie.vote -= 1
    pie.save()
    
    request.session['voted_pies'].remove(pie_id)
    request.session.modified = True
    
    messages.success(request, "Your vote has been removed.", extra_tags='success')
    return redirect('/pies')


# delete pie 
def delete_pie(request, id):
    if 'id' not in request.session:
        messages.error(request, 'You must login first to delete a pie.', extra_tags='login')
        return redirect('/')
    pie = Pie.objects.get(id=id)
    pie.delete()
    messages.success(request, "Pie deleted.", extra_tags='success')
    return redirect('dashboard')




