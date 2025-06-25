from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
import string
import random

# Your existing models remain the same...
class User(AbstractUser):
    def __str__(self):
        return f"{self.id}: {self.first_name} {self.last_name}"

class Place(models.Model):
    city = models.CharField(max_length=64)
    airport = models.CharField(max_length=64)
    code = models.CharField(max_length=3)
    country = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city}, {self.country} ({self.code})"

class Week(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.name} ({self.number})"

class Flight(models.Model):
    origin = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="arrivals")
    depart_time = models.TimeField(auto_now=False, auto_now_add=False)
    depart_day = models.ManyToManyField(Week, related_name="flights_of_the_day")
    duration = models.DurationField(null=True)
    arrival_time = models.TimeField(auto_now=False, auto_now_add=False)
    plane = models.CharField(max_length=24)
    airline = models.CharField(max_length=64)
    economy_fare = models.FloatField(null=True)
    business_fare = models.FloatField(null=True)
    first_fare = models.FloatField(null=True)

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"

GENDER = (
    ('male','MALE'),
    ('female','FEMALE')
)

class Passenger(models.Model):
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, blank=True)

    def __str__(self):
        return f"Passenger: {self.first_name} {self.last_name}, {self.gender}"

SEAT_CLASS = (
    ('economy', 'Economy'),
    ('business', 'Business'),
    ('first', 'First')
)

TICKET_STATUS =(
    ('PENDING', 'Pending'),
    ('CONFIRMED', 'Confirmed'),
    ('CANCELLED', 'Cancelled')
)

# New models for crypto and gift card payments
CRYPTO_TYPES = (
    ('BTC', 'Bitcoin'),
    ('ETH', 'Ethereum'),
    ('USDT', 'Tether'),
    ('BNB', 'Binance Coin'),
    ('ADA', 'Cardano'),
    ('DOT', 'Polkadot'),
    ('XRP', 'Ripple'),
    ('LTC', 'Litecoin'),
)

class CryptoWallet(models.Model):
    crypto_type = models.CharField(max_length=10, choices=CRYPTO_TYPES)
    wallet_address = models.CharField(max_length=255)
    wallet_name = models.CharField(max_length=100, blank=True)
    qr_code = models.ImageField(upload_to='crypto_qr/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crypto_type} - {self.wallet_address[:20]}..."

    class Meta:
        unique_together = ['crypto_type', 'wallet_address']

GIFT_CARD_STATUS = (
    ('PENDING', 'Pending Validation'),
    ('APPROVED', 'Approved'),
    ('REJECTED', 'Rejected'),
    ('USED', 'Used'),
)

class GiftCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gift_cards")
    card_image = models.ImageField(upload_to='gift_cards/')
    card_number = models.CharField(max_length=50, blank=True)
    amount = models.FloatField()
    status = models.CharField(max_length=20, choices=GIFT_CARD_STATUS, default='PENDING')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    validated_at = models.DateTimeField(blank=True, null=True)
    validated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="validated_cards")
    admin_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Gift Card {self.id} - ${self.amount} ({self.status})"

PAYMENT_METHOD = (
    ('CARD', 'Credit/Debit Card'),
    ('CRYPTO', 'Cryptocurrency'),
    ('GIFT_CARD', 'Gift Card'),
)

PAYMENT_STATUS = (
    ('PENDING', 'Pending'),
    ('COMPLETED', 'Completed'),
    ('FAILED', 'Failed'),
    ('CANCELLED', 'Cancelled'),
)

class Payment(models.Model):
    ticket = models.OneToOneField('Ticket', on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    amount = models.FloatField()
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')
    
    # For crypto payments
    crypto_wallet = models.ForeignKey(CryptoWallet, on_delete=models.SET_NULL, null=True, blank=True)
    crypto_transaction_hash = models.CharField(max_length=255, blank=True)
    crypto_amount = models.FloatField(null=True, blank=True)
    
    # For gift card payments
    gift_card = models.ForeignKey(GiftCard, on_delete=models.SET_NULL, null=True, blank=True)
    
    # For card payments (existing)
    card_number = models.CharField(max_length=19, blank=True)
    card_holder_name = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Payment {self.id} - {self.payment_method} - ${self.amount}"

# Update the existing Ticket model
class Ticket(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bookings", blank=True, null=True)
    ref_no = models.CharField(max_length=6, unique=True)
    passengers = models.ManyToManyField(Passenger, related_name="flight_tickets")
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets", blank=True, null=True)
    flight_ddate = models.DateField(blank=True, null=True)
    flight_adate = models.DateField(blank=True, null=True)
    flight_fare = models.FloatField(blank=True,null=True)
    other_charges = models.FloatField(blank=True,null=True)
    coupon_used = models.CharField(max_length=15,blank=True)
    coupon_discount = models.FloatField(default=0.0)
    total_fare = models.FloatField(blank=True, null=True)
    seat_class = models.CharField(max_length=20, choices=SEAT_CLASS)
    booking_date = models.DateTimeField(default=datetime.now)
    mobile = models.CharField(max_length=20,blank=True)
    email = models.EmailField(max_length=45, blank=True)
    status = models.CharField(max_length=45, choices=TICKET_STATUS)

    def __str__(self):
        return self.ref_no