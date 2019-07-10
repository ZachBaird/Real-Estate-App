from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact

# auth is for automatic logging in

# Create your views here.


def login(request):
    if request.method == 'POST':
        # Pull login data from form
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user with given input
        user = auth.authenticate(username=username, password=password)

        # Login user
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out.')
        # Note how the redirect is structured!! We point to a view method by its name!
        return redirect('index')


def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Start validation - check passwords first
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
                return redirect('register')
            else:
                # Check emails
                if User.objects.filter(email=email).exists():
                    messages.error(
                        request, 'Email already being used on a user')
                    return redirect('register')
                else:
                    # Create the user
                    user = User.objects.create_user(
                        username=username, password=password, email=email, first_name=first_name, last_name=last_name)

                    user.save()

                    messages.success(
                        request, 'Your account is registered. Please login.')
                    redirect('login')

                    # Automatically login user code below
                    '''
                    auth.login(request, user)
                    '''
        else:
            # Display error message
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        return redirect('login')
    else:
        return render(request, 'accounts/register.html')


def dashboard(request):
    user_contacts = Contact.objects.order_by(
        '-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }

    return render(request, 'accounts/dashboard.html', context)
