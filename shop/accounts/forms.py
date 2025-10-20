from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser, ActivationCode



class CustomUserCreationForm(UserCreationForm):



    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email

class CustomAuthenticatedForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        }))

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        }))

    def confirm_login_allowed(self, user):
        # Разрешаем входить неактивным пользователя пропуская переопределяя функцию
        pass

class CodeConfirmForm(forms.ModelForm):

    class Meta:
        model = ActivationCode
        fields = ['code']

        code = forms.CharField(label='Код активации', max_length=6, min_length=6,
                               widget=forms.TextInput(attrs={'id': 'code'}))

    def clean_code(self):
        code = self.cleaned_data['code']
        if not code.isdigit():
            raise forms.ValidationError('Код должен содержать только цифры')
        return code