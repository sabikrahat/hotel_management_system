from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.db import connection

from home.models import CustomerModel, UserModel

# Create your views here.
def home(request):
    isLoggedIn = False
    isAdmin = False
    cursor = connection.cursor()
    cursor.execute(
        'SELECT SUM(budget) FROM customers_data')
    total_budget = cursor.fetchall()
    cursor.close()
    print('Bufget: ', total_budget[0][0])
    cursor_2 = connection.cursor()
    cursor_2.execute(
        'SELECT Count(*) FROM customers_data')
    count = cursor_2.fetchall()
    cursor_2.close()
    print('Count: ', count[0][0])
    try:
        user = UserModel.objects.get(email=request.session['email'])
        
        if user is not None:
            isLoggedIn = True
            if user.role == 'Admin':
                isAdmin = True
            else:
                isAdmin = False
        else:
            isLoggedIn = False
        return render(request, 'index.html', {'user': user ,'isLoggedIn': isLoggedIn, 'isAdmin': isAdmin, 'total_budget': total_budget[0][0], 'count': count[0][0]})
    except:
        isLoggedIn = False
        # messages.error(request, 'You need to login first')
        return render(request, 'index.html', {'user': None ,'isLoggedIn': isLoggedIn, 'isAdmin': isAdmin, 'total_budget': total_budget[0][0], 'count': count[0][0]})


def signup(request):
   if request.method == "POST":

        email = request.POST.get('email')
        password = make_password(request.POST.get('password'))

        new_user = UserModel()
        new_user.email = email
        new_user.password = password
        new_user.name = email.split('@')[0]
        new_user.phone = '+8801234567890'
        new_user.role = 'Manager'

        if new_user.isExists():
            messages.error(request, "This Email is already registered")
            return redirect('signup')
        else:
            new_user.save()
            messages.success(request, "Registered Successfully")
            return redirect('login')
   return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        try:
            userDetail = UserModel.objects.get(
                email=request.POST.get('email'))
            if check_password(request.POST.get('password'), (userDetail.password)):
                request.session['email'] = userDetail.email
                return redirect('/')
            else:
                messages.error(
                    request, 'Password incorrect...!')
        except UserModel.DoesNotExist as e:
            messages.error(request, 'No user found of this email....!')
    return render(request, 'login.html')


def logout(request):
    try:
        del request.session['email']
        messages.success(request, "Successfully logged out.")
    except:
        messages.error(request, "An error occurred. Try again.")
        return redirect('/')
    return redirect('/')


def customers(request):
    try:
        user = UserModel.objects.get(email=request.session['email'])
        customers = CustomerModel.objects.raw('SELECT * FROM customers_data')
        return render(request, 'customers.html', {'customers' : customers, 'user' : user})
        
    except:
        messages.error(request, 'You need to login first')
        return redirect('/login')


def order(request):
    try:
        user = UserModel.objects.get(email=request.session['email'])
        if request.method == 'POST':
            if request.POST.get('name') and request.POST.get('email') and request.POST.get('phone') and request.POST.get('capacity')and request.POST.get('budget') and request.POST.get('manager')and request.POST.get('status'):

                order = CustomerModel()
                
                order.name = request.POST.get('name')
                order.email = request.POST.get('email')
                order.phone = request.POST.get('phone')
                order.capacity = request.POST.get('capacity')
                order.budget = request.POST.get('budget')
                order.manager = request.POST.get('manager')
                order.status = request.POST.get('status')

                order.save()

                messages.success(request, "Order Taken")
                return redirect('/')
        else:
            return render(request, 'order.html', {'user' : user})
    except:
        messages.error(request, 'You need to login first')
        return render(request, 'login.html')


def profile(request, token):
    users = UserModel.objects.raw('SELECT * FROM users_data WHERE id = %s', [token])
    user = users[0]
    return render(request, 'profile.html', {'user' : user})

def editProfile(request, token):
    users = UserModel.objects.raw('SELECT * FROM users_data WHERE id = %s', [token])
    user = users[0]
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('phone'):
            user.name = request.POST.get('name')
            user.phone = request.POST.get('phone')
            user.save()
            messages.success(request, "Successfully updated")
            return redirect('/')
    return render(request, 'edit-profile.html', {'user' : user})


def admin(request):
    try:
        user = UserModel.objects.get(email=request.session['email'])
        if user.role == 'Admin':
            users = UserModel.objects.raw('SELECT * FROM users_data')
            return render(request, 'admin.html', {'users' : users, 'user' : user})
        else:
            messages.error(request, 'Only admin users can access')
            return redirect('/')
    except:
        messages.error(request, 'You need to login first')
        return render(request, 'login.html')


def roleChange(request, token):
    users = UserModel.objects.raw('SELECT * FROM users_data WHERE id = %s', [token])
    user = users[0]
    curr_role = user.role
    if curr_role == 'Admin':
        user.role = 'Manager'
    else:
        user.role = 'Admin'
    
    user.save()
    messages.success(request, "Successfully role updated to " + user.role)
    return redirect('/admin')

def termsandcondition(request):
    return render(request, 'terms-and-condition.html')

