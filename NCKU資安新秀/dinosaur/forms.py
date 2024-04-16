from django import forms
from django.contrib.auth.models import User
from .models import Order

class Logi_form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]


# class Register_form(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     username = forms.CharField(max_length=30)
#     class Meta:
#         model = User
#         fields = [
#             'username',
#             'password',
#             'email',
#             'first_name',
#         ]
from django.core.validators import MinLengthValidator
from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.core.validators import RegexValidator

class Register_form(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        validators=[
            MinLengthValidator(10),
            validators.RegexValidator(
                regex='[A-Z]',
                message='Password must contain at least one uppercase letter.',
                code='password_no_upper'
            ),
            validators.RegexValidator(
                regex='[a-z]',
                message='Password must contain at least one lowercase letter.',
                code='password_no_lower'
            ),
            validators.RegexValidator(
                regex='\d',
                message='Password must contain at least one digit.',
                code='password_no_digit'
            ),
            validators.RegexValidator(
                regex='[!@#$%^&*(),.?":{}|<>]',
                message='Password must contain at least one special character.',
                code='password_no_special'
            ),
        ]
    )
    
    username = forms.CharField(max_length=10, validators=[RegexValidator('^[a-zA-Z0-9]+$')])

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'first_name',
        ]

    def clean_password(self):
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')

        # 檢查密碼是否包含敏感模式
        sensitive_patterns = ['randomblob(', 'when not null then 1 else 1 end']
        for pattern in sensitive_patterns:
            if pattern in password or pattern in username:
                raise forms.ValidationError(f"Password or username cannot contain sensitive pattern: {pattern}")

        return password

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # 檢查 username 是否包含敏感模式
        sensitive_pattern = 'randomblob(100000) when not null then 1 else 1 end'
        if sensitive_pattern in username:
            raise forms.ValidationError(f"Username cannot contain sensitive pattern: {sensitive_pattern}")

        return username





class AddForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M:%S%z'],  # 包括时区信息
    )
    
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M:%S%z'],  # 包括时区信息
    )

    class Meta:
        model = Order
        fields = [
            'start_time',
            'end_time',
        ]

class EventForm(forms.Form):
    title = forms.CharField(max_length=100, label='Event Title')
    description = forms.CharField(widget=forms.Textarea, label='Event Description')
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'datetime-local'}), label='Event Date and Time')
