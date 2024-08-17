from django.shortcuts import render, redirect
from django.contrib import auth, messages
from costumers.forms import SingUpForm


def register_user(request):
    """ This function is used to register a new user. """
    if request.method == 'POST':
        form = SingUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            """ Before save is added some permission. """
            user.save()
            auth.login(request, user)
            messages.success(request, 'Your account has been created and logged in.')
            return redirect('home')

        messages.error(request, 'Something went wrong, please try again.')
        return redirect('register_page')

    form = SingUpForm()
    return render(request, 'costumers/auth/register.html', {'form': form})


def login_user(request):
    """ This function is used to login a user. """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login_page')
    return render(request, 'costumers/auth/login.html')


def logout_user(request):
    """ This function is used to logout a user. """
    auth.logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def forgot_password(request):
    """ When a user forgot its password this function is called.(but it works by default for now) """
    return render(request, 'costumers/auth/forgot-password.html')
