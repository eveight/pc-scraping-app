from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegistrationForm(forms.ModelForm):
    email = forms.CharField(label='Введите имэйл',
                            widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Введите пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Введите пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        data = self.cleaned_data
        if data['password2'] != data['password']:
            raise forms.ValidationError('Пароли не совпадают')
        return data['password2']


class UpdateUserForm(forms.ModelForm):
    message = forms.BooleanField(label='Получать рассылку на обновления?',
                                 required=False,
                                 widget=forms.CheckboxInput())

    class Meta:
        model = User
        fields = ('message',)


class Contact(forms.Form):
    comp = forms.CharField(label='Что добавить на сайт?',
                           required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Введите ваш имэйл',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
