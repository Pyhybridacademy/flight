from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta
import json

from flight.models import *
from .models import AdminLog, SystemSettings
from .forms import *

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def dashboard(request):
    # Dashboard statistics
    total_users = User.objects.count()
    total_flights = Flight.objects.count()
    total_bookings = Ticket.objects.count()
    total_payments = Payment.objects.count()
    
    # Recent activity
    recent_bookings = Ticket.objects.order_by('-booking_date')[:10]
    recent_payments = Payment.objects.order_by('-created_at')[:10]
    
    # Monthly statistics
    current_month = timezone.now().replace(day=1)
    monthly_bookings = Ticket.objects.filter(booking_date__gte=current_month).count()
    monthly_revenue = Payment.objects.filter(
        created_at__gte=current_month,
        status='COMPLETED'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Payment method statistics
    payment_stats = Payment.objects.values('payment_method').annotate(
        count=Count('id'),
        total_amount=Sum('amount')
    )
    
    context = {
        'total_users': total_users,
        'total_flights': total_flights,
        'total_bookings': total_bookings,
        'total_payments': total_payments,
        'recent_bookings': recent_bookings,
        'recent_payments': recent_payments,
        'monthly_bookings': monthly_bookings,
        'monthly_revenue': monthly_revenue,
        'payment_stats': payment_stats,
    }
    
    return render(request, 'backoffice/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def user_management(request):
    search_query = request.GET.get('search', '')
    users = User.objects.all()
    
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    return render(request, 'backoffice/user_management.html', {
        'users': users,
        'search_query': search_query
    })

@login_required
@user_passes_test(is_admin)
def flight_management(request):
    search_query = request.GET.get('search', '')
    flights = Flight.objects.all()
    
    if search_query:
        flights = flights.filter(
            Q(airline__icontains=search_query) |
            Q(plane__icontains=search_query) |
            Q(origin__city__icontains=search_query) |
            Q(destination__city__icontains=search_query)
        )
    
    paginator = Paginator(flights, 20)
    page_number = request.GET.get('page')
    flights = paginator.get_page(page_number)
    
    return render(request, 'backoffice/flight_management.html', {
        'flights': flights,
        'search_query': search_query
    })

@login_required
@user_passes_test(is_admin)
def booking_management(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    bookings = Ticket.objects.all().order_by('-booking_date')
    
    if search_query:
        bookings = bookings.filter(
            Q(ref_no__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    paginator = Paginator(bookings, 20)
    page_number = request.GET.get('page')
    bookings = paginator.get_page(page_number)
    
    return render(request, 'backoffice/booking_management.html', {
        'bookings': bookings,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': Ticket.STATUS_CHOICES if hasattr(Ticket, 'STATUS_CHOICES') else []
    })

@login_required
@user_passes_test(is_admin)
def payment_management(request):
    search_query = request.GET.get('search', '')
    method_filter = request.GET.get('method', '')
    status_filter = request.GET.get('status', '')
    
    payments = Payment.objects.all().order_by('-created_at')
    
    if search_query:
        payments = payments.filter(
            Q(ticket__ref_no__icontains=search_query) |
            Q(ticket__user__username__icontains=search_query)
        )
    
    if method_filter:
        payments = payments.filter(payment_method=method_filter)
    
    if status_filter:
        payments = payments.filter(status=status_filter)
    
    paginator = Paginator(payments, 20)
    page_number = request.GET.get('page')
    payments = paginator.get_page(page_number)
    
    return render(request, 'backoffice/payment_management.html', {
        'payments': payments,
        'search_query': search_query,
        'method_filter': method_filter,
        'status_filter': status_filter,
        'method_choices': Payment.PAYMENT_METHOD_CHOICES if hasattr(Payment, 'PAYMENT_METHOD_CHOICES') else [],
        'status_choices': Payment.STATUS_CHOICES if hasattr(Payment, 'STATUS_CHOICES') else []
    })

@login_required
@user_passes_test(is_admin)
def crypto_wallet_management(request):
    wallets = CryptoWallet.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = CryptoWalletForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Crypto wallet added successfully!')
            return redirect('backoffice:crypto_wallet_management')
    else:
        form = CryptoWalletForm()
    
    return render(request, 'backoffice/crypto_wallet_management.html', {
        'wallets': wallets,
        'form': form
    })

@login_required
@user_passes_test(is_admin)
def gift_card_management(request):
    status_filter = request.GET.get('status', '')
    gift_cards = GiftCard.objects.all().order_by('-uploaded_at')
    
    if status_filter:
        gift_cards = gift_cards.filter(status=status_filter)
    
    paginator = Paginator(gift_cards, 20)
    page_number = request.GET.get('page')
    gift_cards = paginator.get_page(page_number)
    
    return render(request, 'backoffice/gift_card_management.html', {
        'gift_cards': gift_cards,
        'status_filter': status_filter,
        'status_choices': GiftCard.STATUS_CHOICES if hasattr(GiftCard, 'STATUS_CHOICES') else []
    })

@login_required
@user_passes_test(is_admin)
def validate_gift_card(request, card_id):
    if request.method == 'POST':
        card = get_object_or_404(GiftCard, id=card_id)
        action = request.POST.get('action')
        notes = request.POST.get('notes', '')
        
        if action == 'approve':
            card.status = 'APPROVED'
            card.validated_by = request.user
            card.validated_at = timezone.now()
            card.admin_notes = notes
            card.save()
            messages.success(request, f'Gift card #{card.id} approved successfully!')
        elif action == 'reject':
            card.status = 'REJECTED'
            card.validated_by = request.user
            card.validated_at = timezone.now()
            card.admin_notes = notes
            card.save()
            messages.success(request, f'Gift card #{card.id} rejected successfully!')
        
        # Log the action
        AdminLog.objects.create(
            user=request.user,
            action=f'Gift Card {action.title()}',
            model_name='GiftCard',
            object_id=str(card.id),
            details=f'Status changed to {card.status}. Notes: {notes}'
        )
    
    return redirect('backoffice:gift_card_management')

@login_required
@user_passes_test(is_admin)
def verify_crypto_payment(request, payment_id):
    if request.method == 'POST':
        payment = get_object_or_404(Payment, id=payment_id)
        action = request.POST.get('action')
        notes = request.POST.get('notes', '')
        
        if action == 'approve':
            payment.status = 'COMPLETED'
            payment.ticket.status = 'CONFIRMED'
            payment.ticket.booking_date = timezone.now()
            payment.ticket.save()
            payment.save()
            messages.success(request, f'Crypto payment #{payment.id} verified and approved!')
        elif action == 'reject':
            payment.status = 'FAILED'
            payment.save()
            messages.success(request, f'Crypto payment #{payment.id} rejected!')
        
        # Log the action
        AdminLog.objects.create(
            user=request.user,
            action=f'Crypto Payment {action.title()}',
            model_name='Payment',
            object_id=str(payment.id),
            details=f'Status changed to {payment.status}. Notes: {notes}'
        )
    
    return redirect('backoffice:payment_management')

@login_required
@user_passes_test(is_admin)
def reports(request):
    # Date range filter
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if not start_date:
        start_date = (timezone.now() - timedelta(days=30)).date()
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    
    if not end_date:
        end_date = timezone.now().date()
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    # Revenue report
    revenue_data = Payment.objects.filter(
        created_at__date__range=[start_date, end_date],
        status='COMPLETED'
    ).aggregate(
        total_revenue=Sum('amount'),
        total_transactions=Count('id')
    )
    
    # Booking statistics
    booking_stats = Ticket.objects.filter(
        booking_date__date__range=[start_date, end_date]
    ).values('status').annotate(count=Count('id'))
    
    # Payment method breakdown
    payment_breakdown = Payment.objects.filter(
        created_at__date__range=[start_date, end_date]
    ).values('payment_method').annotate(
        count=Count('id'),
        total_amount=Sum('amount')
    )
    
    # Popular routes
    popular_routes = Ticket.objects.filter(
        booking_date__date__range=[start_date, end_date]
    ).values(
        'flight__origin__city',
        'flight__destination__city'
    ).annotate(count=Count('id')).order_by('-count')[:10]
    
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'revenue_data': revenue_data,
        'booking_stats': booking_stats,
        'payment_breakdown': payment_breakdown,
        'popular_routes': popular_routes,
    }
    
    return render(request, 'backoffice/reports.html', context)

@login_required
@user_passes_test(is_admin)
def system_settings(request):
    settings = SystemSettings.objects.all()
    
    if request.method == 'POST':
        form = SystemSettingsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Setting saved successfully!')
            return redirect('backoffice:system_settings')
    else:
        form = SystemSettingsForm()
    
    return render(request, 'backoffice/system_settings.html', {
        'settings': settings,
        'form': form
    })

@login_required
@user_passes_test(is_admin)
def admin_logs(request):
    logs = AdminLog.objects.all().order_by('-timestamp')
    
    paginator = Paginator(logs, 50)
    page_number = request.GET.get('page')
    logs = paginator.get_page(page_number)
    
    return render(request, 'backoffice/admin_logs.html', {
        'logs': logs
    })

# AJAX Views
@login_required
@user_passes_test(is_admin)
def toggle_user_status(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.is_active = not user.is_active
        user.save()
        
        AdminLog.objects.create(
            user=request.user,
            action='User Status Toggle',
            model_name='User',
            object_id=str(user.id),
            details=f'User {user.username} status changed to {"Active" if user.is_active else "Inactive"}'
        )
        
        return JsonResponse({
            'success': True,
            'is_active': user.is_active,
            'message': f'User {user.username} {"activated" if user.is_active else "deactivated"} successfully!'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
@user_passes_test(is_admin)
def toggle_wallet_status(request, wallet_id):
    if request.method == 'POST':
        wallet = get_object_or_404(CryptoWallet, id=wallet_id)
        wallet.is_active = not wallet.is_active
        wallet.save()
        
        AdminLog.objects.create(
            user=request.user,
            action='Crypto Wallet Status Toggle',
            model_name='CryptoWallet',
            object_id=str(wallet.id),
            details=f'Wallet {wallet.crypto_type} status changed to {"Active" if wallet.is_active else "Inactive"}'
        )
        
        return JsonResponse({
            'success': True,
            'is_active': wallet.is_active,
            'message': f'Wallet {"activated" if wallet.is_active else "deactivated"} successfully!'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
@user_passes_test(is_admin)
def get_dashboard_stats(request):
    """AJAX endpoint for dashboard statistics"""
    stats = {
        'total_users': User.objects.count(),
        'total_flights': Flight.objects.count(),
        'total_bookings': Ticket.objects.count(),
        'pending_payments': Payment.objects.filter(status='PENDING').count(),
        'pending_gift_cards': GiftCard.objects.filter(status='PENDING').count(),
    }
    
    return JsonResponse(stats)