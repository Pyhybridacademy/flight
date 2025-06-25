from django.urls import path
from . import views

app_name = 'backoffice'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # User Management
    path('users/', views.user_management, name='user_management'),
    path('users/toggle-status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    
    # Flight Management
    path('flights/', views.flight_management, name='flight_management'),
    
    # Booking Management
    path('bookings/', views.booking_management, name='booking_management'),
    
    # Payment Management
    path('payments/', views.payment_management, name='payment_management'),
    path('payments/verify-crypto/<int:payment_id>/', views.verify_crypto_payment, name='verify_crypto_payment'),
    
    # Crypto Wallet Management
    path('crypto-wallets/', views.crypto_wallet_management, name='crypto_wallet_management'),
    path('crypto-wallets/toggle-status/<int:wallet_id>/', views.toggle_wallet_status, name='toggle_wallet_status'),
    
    # Gift Card Management
    path('gift-cards/', views.gift_card_management, name='gift_card_management'),
    path('gift-cards/validate/<int:card_id>/', views.validate_gift_card, name='validate_gift_card'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
    
    # System Settings
    path('settings/', views.system_settings, name='system_settings'),
    
    # Admin Logs
    path('logs/', views.admin_logs, name='admin_logs'),
    
    # AJAX endpoints
    path('api/dashboard-stats/', views.get_dashboard_stats, name='dashboard_stats'),
]