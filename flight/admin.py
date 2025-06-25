from django.contrib import admin
from django.utils import timezone
from .models import *

# Register your existing models here
admin.site.register(User)
admin.site.register(Place)
admin.site.register(Flight)
admin.site.register(Week)
admin.site.register(Passenger)
admin.site.register(Ticket)

@admin.register(CryptoWallet)
class CryptoWalletAdmin(admin.ModelAdmin):
    list_display = ['crypto_type', 'wallet_address', 'is_active', 'created_at']
    list_filter = ['crypto_type', 'is_active', 'created_at']
    search_fields = ['wallet_address']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Wallet Information', {
            'fields': ('crypto_type', 'wallet_address', 'qr_code')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(GiftCard)
class GiftCardAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'status', 'uploaded_at', 'validated_at']
    list_filter = ['status', 'uploaded_at', 'validated_at']
    search_fields = ['user__username', 'user__email', 'card_number']
    readonly_fields = ['uploaded_at', 'validated_at']
    
    fieldsets = (
        ('Card Information', {
            'fields': ('user', 'card_image', 'card_number', 'amount')
        }),
        ('Validation', {
            'fields': ('status', 'admin_notes', 'validated_by')
        }),
        ('Timestamps', {
            'fields': ('uploaded_at', 'validated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            if obj.status in ['APPROVED', 'REJECTED']:
                obj.validated_by = request.user
                obj.validated_at = timezone.now()
        super().save_model(request, obj, form, change)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'payment_method', 'amount', 'status', 'created_at']
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['ticket__ref_no', 'ticket__user__username']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('ticket', 'payment_method', 'amount', 'status')
        }),
        ('Card Details', {
            'fields': ('card_number', 'card_holder_name'),
            'classes': ('collapse',)
        }),
        ('Crypto Details', {
            'fields': ('crypto_wallet', 'crypto_transaction_hash', 'crypto_amount'),
            'classes': ('collapse',)
        }),
        ('Gift Card Details', {
            'fields': ('gift_card',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )