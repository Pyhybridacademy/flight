from django import forms
from .models import GiftCard, Payment

class GiftCardUploadForm(forms.ModelForm):
    class Meta:
        model = GiftCard
        fields = ['card_image', 'card_number', 'amount']
        widgets = {
            'card_image': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            }),
            'card_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter gift card number (optional)'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter gift card amount',
                'step': '0.01',
                'min': '0'
            })
        }

class CryptoPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['crypto_transaction_hash', 'crypto_amount']
        widgets = {
            'crypto_transaction_hash': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter transaction hash'
            }),
            'crypto_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Amount sent',
                'step': '0.00000001',
                'min': '0'
            })
        }