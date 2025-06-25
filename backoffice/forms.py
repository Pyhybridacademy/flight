from django import forms
from django.contrib.auth.models import User
from flight.models import *
from .models import SystemSettings

class CryptoWalletForm(forms.ModelForm):
    class Meta:
        model = CryptoWallet
        fields = ['crypto_type', 'wallet_address', 'qr_code', 'is_active']
        widgets = {
            'crypto_type': forms.Select(attrs={'class': 'form-control'}),
            'wallet_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter wallet address'}),
            'qr_code': forms.FileInput(attrs={'class': 'form-control-file'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = '__all__'
        widgets = {
            'airline': forms.TextInput(attrs={'class': 'form-control'}),
            'plane': forms.TextInput(attrs={'class': 'form-control'}),
            'origin': forms.Select(attrs={'class': 'form-control'}),
            'destination': forms.Select(attrs={'class': 'form-control'}),
            'depart_day': forms.Select(attrs={'class': 'form-control'}),
            'depart_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'arrival_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'economy_fare': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'business_fare': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'first_fare': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SystemSettingsForm(forms.ModelForm):
    class Meta:
        model = SystemSettings
        fields = ['key', 'value', 'description']
        widgets = {
            'key': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Setting key'}),
            'value': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Setting value'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Description (optional)'}),
        }

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = '__all__'
        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'airport': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '3'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }

class GiftCardValidationForm(forms.Form):
    action = forms.ChoiceField(
        choices=[('approve', 'Approve'), ('reject', 'Reject')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Admin notes (optional)'})
    )

class PaymentVerificationForm(forms.Form):
    action = forms.ChoiceField(
        choices=[('approve', 'Approve'), ('reject', 'Reject')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Admin notes (optional)'})
    )