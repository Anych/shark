from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class Emails:
    def __init__(self, order=None, user=None, email=None, question=None,
                 product_url=None, pk=None, command=None):
        self.order = order
        self.user = user
        self.email = email
        self.question = question
        self.product_url = product_url
        self.pk = pk
        self.command = command
        self.mail_subject = None
        self.message = None
        self.redirect_to_function()

    def redirect_to_function(self):
        if self.user is not None:
            if self.question is not None:
                self.question_email()

            elif self.order is not None:
                self.order_email()

            elif self.pk is not None:
                if self.command == 'forgot':
                    self.forgot_password()
                elif self.command == 'confirm' or self.command == 'register':
                    self.confirm_email()

        else:
            self.new_order_email()

    def question_email(self):
        self.mail_subject = 'Новый вопрос на сайте'
        self.message = render_to_string('accounts/question_email.html', {
            'name': self.user,
            'email': self.email,
            'question': self.question,
            'product_url': self.product_url,
        })
        self.send_email_to_admins()

    def new_order_email(self):
        self.mail_subject = 'Новый заказ на сайте'
        self.message = render_to_string('accounts/new_order.html', {'order_id': self.order})
        self.send_email_to_admins()

    def order_email(self):
        self.mail_subject = 'Спасибо за покупку!'
        self.message = render_to_string('orders/order_received_email.html', {'user': self.user, 'order': self.order})
        self.send_email_to_user()

    def confirm_email(self):
        self.mail_subject = 'Подтверждение почты'
        self.message = render_to_string('accounts/account_verification_email.html', {
            'user': self.user,
            'uid': urlsafe_base64_encode(force_bytes(self.pk)),
            'token': default_token_generator.make_token(self.user),
            'email': self.email,
            'command': self.command,
        })
        self.send_email_to_user()

    def forgot_password(self):
        self.mail_subject = 'Восстановление пароля'
        self.message = render_to_string('accounts/reset_password_email.html', {
            'user': self.user,
            'uid': urlsafe_base64_encode(force_bytes(self.pk)),
            'token': default_token_generator.make_token(self.user)
        })
        self.send_email_to_user()

    def send_email_to_admins(self):
        send_mass_mail = EmailMessage(self.mail_subject, self.message, to=[
            'mila-iris@mila-iris.kz',
            'anuar123@mail.ru',
            'botaonelove@yandex.ru',
            'anuar.umarov@gmail.com'])
        send_mass_mail.send()

    def send_email_to_user(self):
        send_email = EmailMessage(self.mail_subject, self.message, to=[self.email])
        send_email.send()
