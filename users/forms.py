from django import forms

from users.models import CustomUser


class UserRegisterForm(forms.ModelForm):
    """Форма регистрации пользователя"""

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone', 'email', 'avatar')

        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'phone': 'Телефон',
            'email': 'Email',
            'avatar': 'Аватар',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
