from django import forms
from .models import Order

class OrderCreationForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'address': 'Адрес',
            'postal_code': 'Почтовый индекс',
            'city': 'Город'
        }