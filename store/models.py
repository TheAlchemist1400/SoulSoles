from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from cloudinary.models import CloudinaryField 

# Create your models here.
class Sneaker(models.Model):
    name = models.CharField(max_length = 100)
    short_description = models.TextField(max_length = 350, blank = True)
    description = models.TextField()
    image = CloudinaryField('image')
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # original price
    on_sale = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
class SneakerSize(models.Model):
    sneaker = models.ForeignKey(Sneaker, related_name='sizes', on_delete = models.CASCADE)
    size = models.CharField(max_length= 5)
    price = models.DecimalField(max_digits = 8, decimal_places = 2, null = True, blank = True)
    is_sold_out = models.BooleanField(default = False)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def is_on_sale(self):
        return self.original_price and self.original_price > self.price

    def __str__(self):
        return f"{self.sneaker.name} - Size {self.size}"
    
    def __str__(self):
        return f"{self.sneaker.name} - Size {self.size}"
    
class SneakerImage(models.Model):
    sneaker = models.ForeignKey(Sneaker, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')   
    
    def __str__(self):
        return f"Extra image for {self.sneaker.name}"
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)
    sneaker_size = models.ForeignKey('SneakerSize', on_delete = models.CASCADE)
    quantity  = models.PositiveIntegerField(default = 1)
    added_at = models.DateTimeField(auto_now_add = True)
    
    @property
    def subtotal(self):
        return self.sneaker_size.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.sneaker_size} in {self.user or 'Guest'}'s Cart"
    
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
User = settings.AUTH_USER_MODEL

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending_payment', 'Pending Payment'),
        ('funds_held', 'Funds Held (Escrow)'),
        ('shipped', 'Order Shipped'),
        ('delivered', 'Order Delivered'),
        ('released', 'Funds Successfully Released to SoulSoles.co'),
        ('refunded', 'Refunded'),
        ('disputed', 'In Dispute'),
    ]
    # Variables for Esrcow function
    buyer = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE) 
    total = models.DecimalField(max_digits=10, decimal_places=2)  
    created_at = models.DateTimeField(auto_now_add=True)  
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending_payment')
    payment_reference = models.CharField(max_length=200, blank=True)
    tracking_number = models.CharField(max_length=200, blank=True)
    courier = models.CharField(max_length=200, blank=True)
    released_at = models.DateTimeField(null=True, blank=True)
    
    # Escrow Functions
    
    # save when funds are held
    def mark_funds_held(self, ref=None):
        self.status = 'funds_held'
        if ref:
            self.payment_reference = ref
            self.save()
            
    # save when order is shipped 
    def mark_shipped(self, courier = None, tracking=None):
        self.status = 'shipped'        
        if courier:
            self.courier = courier
        if tracking:
            self.tracking_number = tracking
        self.save()
        
    # save when order is delivered 
    def mark_delivered(self):
        self.status = 'released'
        self.save()
    
    # Function to release the funds
    def release_funds(self):
        self.status = 'released'
        self.released_at = timezone.now()
        self.save()
        
    # save if order is refunded, after appeal
    def mark_refund(self):
        self.status = 'refund'
        self.save()
        
    def __str__(self):
        return f"Order #{self.pk} - {self.buyer} - {self.status}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)    
    sneaker_size = models.ForeignKey(SneakerSize, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"{self.sneaker_size.sneaker.name} - Size {self.sneaker_size.size} (x{self.quantity})"
             
class SourcingRequest(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    sneaker_name = models.CharField(max_length = 200)
    sizes = models.CharField(max_length = 100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f"{self.sneaker_name} - Sizes {self.sizes} (by{self.user})"
                