from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contacts


# Signup
def signup(request):
    if request.method == 'POST':
        # Register user
        # Get values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # password check
        if password == password2:
            # Check username unique
            if User.objects.filter(username=username).exists():
                messages.error(request, 'username is already taken')
                return redirect('signup')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'email is already taken')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                    #login after signup
                    # auth.login(request, user)
                    # messages.success(request, 'you are logged in')
                    # return redirect('index')
                    user.save()
                    messages.success(request, 'done, please login')
                    return redirect('login')

        else:
            messages.error(request, 'passwords not match')
            return redirect('signup')
    else:
        return render(request, 'accounts/signup.html')


# Login
def login(request):
    if request.user.is_authenticated:
        messages.error(request, 'please log out')
        return redirect('index')
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request,'ops')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


# Logout
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'you are now logged out')
        return redirect('index')

# Dashboard
def dashboard(request):
    user_contact = Contacts.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts': user_contact,
    }
    return render(request, 'accounts/dashboard.html', context)
