from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class RegistrationUserForm(forms.ModelForm):
    password_1 = forms.CharField(widget=forms.PasswordInput(), label='Введите пароль')
    password_2 = forms.CharField(widget=forms.PasswordInput(), label='Повторите пароль')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password_1'] != cleaned_data['password_2']:
            # raise forms.ValidationError('Пароли не совпадают')
            self.add_error('password_1', 'Пароли не совпадают')

    class Meta:
        model = User
        fields = \
            [
                'username',
                'first_name',
                'last_name',
                'email',
            ]
