from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.views import View
from user.forms import SingUpForm
from django.urls import reverse_lazy
from config.settings import EMAIL_DEFAULT_SENDER
from user.token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from user.models import User
from django.contrib.auth import login
from django.http import HttpResponse


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
            message = render_to_string('user/acc_active_email.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(
                'Activate your blog account.',
                message,
                EMAIL_DEFAULT_SENDER,
                [user.email],
                fail_silently=False

            )
            messages.success(request, 'Your account has been created and logged in.')
            return render(request, 'user/confirm_activate_account.html')
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
            return redirect('login_page')


class LogoutUserView(View):
    """ This class is used to logout a user. """

    def get(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect(reverse_lazy('home'))


def forgot_password(request):
    """ When a user forgot its password this function is called.(but it works by default for now) """
    return render(request, 'user/forgot-password.html')


class AccountActivationView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Your account has been activated.')
            return redirect('home')
        else:
            return HttpResponse('Activation link is invalid!')
