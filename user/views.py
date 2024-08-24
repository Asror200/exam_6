from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.views import View
from user.forms import SingUpForm
from django.urls import reverse_lazy
from config.settings import EMAIL_DEFAULT_SENDER


class RegisterUserView(View):
    """ This class is used to register a new user. """

    def get(self, request):
        form = SingUpForm()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = SingUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            send_mail(
                'Successfully Registered',
                'Thank you for creating your account!',
                EMAIL_DEFAULT_SENDER,
                [user.email],
                fail_silently=False

            )
            messages.success(request, 'Your account has been created and logged in.')
            return redirect('home')
        messages.error(request, 'Something went wrong, please try again.')
        return redirect('register_page')


class LoginUserView(View):
    """ This class is used to login a user. """

    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(email=email, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('home')
            messages.error(request, 'Invalid email or password')


class LogoutUserView(View):
    """ This class is used to logout a user. """

    def get(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect(reverse_lazy('home'))


def forgot_password(request):
    """ When a user forgot its password this function is called.(but it works by default for now) """
    return render(request, 'user/forgot-password.html')
