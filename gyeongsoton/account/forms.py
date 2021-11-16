from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "type": "username",
                "placeholder": "ID",
            }
        ),
        label="Username",
        error_messages={
            "unique": "입력하신 이름을 사용하는 유저가 이미 존재합니다.",
            "max_length": "이름은 최대 150글자까지 작성할 수 있습니다.",
        },
    )

    password1 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "type": "password",
                "placeholder": "비밀번호",
            }
        ),
        label="password",
    )

    password2 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "type": "password",
                "placeholder": "비밀번호 확인",
            }
        ),
        label="password",
    )

    nickname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "type": "nickname",
                "placeholder": "닉네임",
            }
        ),
        label="enter nickname",
        error_messages={"unique": "입력하신 닉네임을 사용하는 유저가 이미 존재합니다."},
    )

    error_messages = {
        "password_mismatch": "입력하신 두 비밀번호가 같지 않습니다.",
    }

    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2", "nickname", "age", "sex"]


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class':'validate',
            'placeholder': 'ID'
            }
        )
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'비밀번호'}))