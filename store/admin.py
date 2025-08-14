from django.contrib import admin
from .models import Sneaker, SneakerSize, SneakerImage, CartItem, Order, OrderItem, SourcingRequest # Import models so they can be used in django administration

# Register your models here.
class SneakerSizeInline(admin.TabularInline):
    model = SneakerSize
    extra = 1
    
@admin.register(Sneaker)  
class SneakerAdmin(admin.ModelAdmin):
    inlines = [SneakerSizeInline]    
    list_display = ['name', 'on_sale']
    list_editable = ('on_sale',)
    fields = ['name', 'short_description', 'description', 'image', 'on_sale']
    
@admin.register(SneakerImage)
class SneakerImageAdmin(admin.ModelAdmin):
    list_display = ( 'sneaker', 'image') 
    
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'sneaker_size', 'quantity', 'added_at')
    list_filter = ('user',)    
    
@admin.register(Order)
class OrderAdmin (admin.ModelAdmin):
    list_display = ('id', 'buyer', 'status', 'total', 'created_at')
    list_filter = ('created_at', 'status')   
    search_fields = ('buyer_username',) 
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'sneaker_size', 'quantity', 'price')
    list_filter = ('order',)
    
@admin.register(SourcingRequest)   
class SourcingRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'sneaker_name', 'sizes', 'created_at') 
    list_filter = ('created_at',)
    search_fields = ('sneaker_name', 'user_username')
        
#admin.site.register(Sneaker, SneakerAdmin)    
#admin.site.register(SneakerImage)
    