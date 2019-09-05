from django import forms

from .models import User


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'avatar',
            'description',
            'status',
            # 'gender',
            'phone'
        ]
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Электронная почта',
            'avatar': 'Аватар',
            'description': 'Информация',
            'status': 'Статус',
            # 'gender': 'Пол',
            'phone': 'Телефон',
        }


class UserPasswordChangeForm(forms.ModelForm):
    old_password = forms.CharField(label="Старый пароль", strip=False, widget=forms.PasswordInput)
    password = forms.CharField(label="Новый пароль", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", strip=False, widget=forms.PasswordInput)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Старый пароль неверен')
        return old_password

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if self.instance.check_password(password):
            raise forms.ValidationError('Новый пароль совпадает со старым')
        return password

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают')
        return password_confirm

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['old_password', 'password', 'password_confirm']
        labels = {
            'old_password': 'Старый пароль',
            'password': 'Пароль',
            'password_confirm': 'Подтверждение пароля',
        }


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Подтвердите пароль', strip=False, widget=forms.PasswordInput)

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают')
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Логин',
            'password': 'Пароль',
            'password_confirm': 'Подтверждение пароля',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Электронная почта',
        }


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', strip=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': 'Логин',
            'password': 'Пароль',
        }
