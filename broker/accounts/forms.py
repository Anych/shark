from django import forms
from django.contrib.auth.password_validation import get_default_password_validators
from django.core.exceptions import ValidationError

from .models import Account, UserProfile


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите Имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите Фамилию'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Введите телефон'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите почту'

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Подтвердите пароль',
    }))

    def clean(self, password_validators=None):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        errors = []
        if password_validators is None:
            password_validators = get_default_password_validators()
        for validator in password_validators:
            try:
                validator.validate(password)
            except ValidationError as error:
                errors.append(error)
        if errors:
            raise ValidationError(errors)

    def clean_email(self):
        email = self.cleaned_data['email']
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError('Данный почтовый ящик уже зарегистрирован в системе')
        return email


class UserForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number', 'email')


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('address', 'city', 'state', 'country', 'profile_picture')

    profile_picture = forms.ImageField(required=False,
                                       error_messages={'Ошибка': "Можно загружать только картинки"},
                                       widget=forms.FileInput)
