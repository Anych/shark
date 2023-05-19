from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView

from .emails import Emails
from .forms import RegistrationForm
from .mixins import TokenMixin
from .models import Account
from .utils import _profile, _redirect_to_next_page


class RegisterView(CreateView):
    form_class = RegistrationForm
    model = Account

    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        context = {'form': form}

        return render(request, 'accounts/register.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email
            user = Account.objects.create_user(first_name=first_name,
                                               last_name=last_name,
                                               email=email,
                                               username=username,
                                               password=password)
            user.phone_number = phone_number
            user.save()

            _profile(user)
            user = auth.authenticate(request=request, email=email, password=password)

            if user is not None:
                auth.login(request, user)
                Emails(user=user, pk=user.pk, email=user.email, command='register')
                return redirect('category_main')
        context = {'form': form}

        return render(request, 'accounts/register.html', context)


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/login.html')

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(request=request, username=email, password=password)

        if user is not None:
            auth.login(request, user)
            try:
                _redirect_to_next_page(request)
            except Exception as e:
                return redirect('category_main')

        else:
            messages.error(request, 'Неправильно введена почта или пароль')

            return redirect('login')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'Вы успешно вышли из системы')

        return redirect('login')


class ConfirmEmailView(View):
    def dispatch(self, request, *args, **kwargs):
        self.request_user = request.user

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.request_user.email:
            Emails(user=self.request_user, pk=self.request_user.pk, email=self.request_user.email, command='confirm')

            return render(request, 'accounts/confirm_email.html')
        else:
            return render(request, 'accounts/confirm_email.html', context={'user': self.request_user})

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        Emails(user=self.request_user, pk=self.request_user.pk, email=email, command='confirm')

        return redirect('category_main')


class ForgotPasswordView(View):
    """View for registered user, if forgot password."""
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/forgot_password.html')

    def post(self, request, *args, **kwargs):
        email = request.POST['email']

        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            Emails(user=user, email=email, pk=user.pk, command='forgot').forgot_password()
            messages.success(request, 'Письмо с инструкцией отправлено на вашу почту')

            return redirect('login')

        else:
            messages.error(request, 'Пользователь с такой почтой не зарегистрирован!')

            return redirect('forgot_password')


class ResetPasswordView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/reset_password.html')

    def post(self, request, *args, **kwargs):
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Пароль успешно сброшен!')

            return redirect('login')


class ChangePasswordView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(pk__exact=request.user.pk)
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Ваш пароль успешно обновлён!')
                return redirect('login')
            else:
                messages.error(request, 'Текущий пароль введен не правильно.')
                return redirect('dashboard')
        else:
            messages.error(request, 'Введенные пароли не совпадают.')
            return redirect('dashboard')


class ResetPasswordValidateView(TokenMixin, View):
    def get(self, request, *args, **kwargs):
        if self.user is not None and default_token_generator.check_token(self.user, kwargs['token']):
            request.session['uid'] = self.uid
            messages.success(request, 'Пожалуйста сбросьте Ваш пароль')

            return redirect('reset_password')
        else:
            messages.error(request, 'Ссылка устарела')

            return redirect('login')


class ConfirmAccountView(TokenMixin, View):
    def get(self, request, *args, **kwargs):

        if self.user is not None and default_token_generator.check_token(self.user, kwargs['token']):
            self.user.email = kwargs['email']
            self.user.confirm_email = True
            self.user.save()
            messages.success(request, 'Поздравляем, Вы успешно подтвердили свою почту!')
            if kwargs['command'] == 'register':

                return redirect('category_main')
            else:

                return redirect('checkout')
        else:
            messages.error(request, 'Ошибка активации!')

            return redirect('register')
