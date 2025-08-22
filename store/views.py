from django.shortcuts import render, get_object_or_404, redirect
from .models import Sneaker, SneakerSize, CartItem, Order, OrderItem, SourcingRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import LoginForm, RegisterForm, SourcingRequestForm

# Home page view
def home(request):
    return render(request, 'store/home.html')

# How page view
def how_it_works(request):
    return render(request, 'store/how_it_works.html')


# Sourcing page view
#def sourcing(request):
#   return render(request, 'store/sourcing.html')


# Checkout uccesful page view
def checkout_successful(request, order_id):
    order = get_object_or_404(Order, id = order_id, buyer = request.user)
    return render(request, 'store/checkout_successful.html', {'order': order})

# Shop page view to list all sneakers
def shop(request):
    sneakers = Sneaker.objects.all()
    return render(request, 'store/shop.html', {'sneakers': sneakers})
    print("Available sizes for:", sneaker.name, available_sizes)  # DEBUG

# Sneaker detail page view showing sneaker info and available sizes
def sneaker_detail(request, pk):
    sneaker = get_object_or_404(Sneaker, pk=pk)
    images = sneaker.images.all()

    # Get all sizes that are NOT sold out
    available_sizes = [size for size in sneaker.sizes.all() if not size.is_sold_out]
    first_available_size = available_sizes[0] if available_sizes else None
    has_available_size = len(available_sizes) > 0

    return render(request, 'store/sneaker_detail.html', {
        'sneaker': sneaker,
        'images': images,
        'has_available_size': has_available_size,
        'first_available_size': first_available_size,
        'available_sizes': available_sizes
    })

# Add selected sneaker size to cart (only for logged-in users)
@login_required
def add_to_cart(request, size_id):
    sneaker_size = get_object_or_404(SneakerSize, id=size_id)

    # Get existing cart item or create a new one with quantity 1
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        sneaker_size=sneaker_size,
        defaults={'quantity': 1}
    )
    
    if not created:
        # If item already in cart, increase quantity by 1
        cart_item.quantity += 1  # Fixed typo here
        cart_item.save()

    # Redirect user to the cart page after adding item
    return redirect('view_cart')

# Display all items in the user's cart
@login_required
def view_cart(request):
    # Get all cart items for the current logged-in user
    cart_items = CartItem.objects.filter(user = request.user)

    # Calculate total price by summing subtotal of each cart item
    total = sum(item.subtotal for item in cart_items)

    # Render the cart template with cart items and total price
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })
# Remove an item from cart
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('view_cart')

@login_required
def checkout(request):
    #cart = request.session.get('cart', []) This is perfect if loggin in wasnt required, records cart current session
    cart_items = CartItem.objects.filter(user = request.user)
    
    # Stops checking out if cart empty
    if not cart_items :
        messages.info(request, "Shopping cart is empty, please add a item.")
        return redirect('shop')
    
    # calculate total price of cart
    total = sum(item.subtotal for item in cart_items)
    
    if request.method == 'POST':  # If user has sent data to the server
        name = request.POST.get('name') # When user presses check out their data ('name') is saved in database
        address = request.POST.get('address')
        
        # create a new order
        order = Order.objects.create(
            buyer = request.user,
            total = total,
            status = 'pending_payment'
        )
        
        # Add all cart items to OrderItem table
        for item in cart_items:
            OrderItem.objects.create(
                order = order,
                sneaker_size = item.sneaker_size,
                quantity = item.quantity,
                price = item.sneaker_size.price   
            )
        
        # Clear cart
        cart_items.delete()
        
        # Notify user
        messages.success(request, 'Order successfully placed! Please complete payment.')
        
       # Redirects users to checkout_successful page after purchase
        return redirect('checkout_successful', order_id = order.id)     
    
    context = {
        'cart': cart_items,
        'total': total,
    }
    return render(request, 'store/checkout.html', context)

def login_view(request):
    # Return user to home page if already logged in
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # check if user exist first
            if not User.objects.filter(username=username).exists():
                messages.error(request, "User does not exit. Please register first.")
                return redirect('register') # Redirects to registeration  page
            
            user = authenticate(request, username = username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Logged in successfully, welcome {user.username}')
                return redirect ('home')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'store/login.html', {'form':form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have logged out")
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(form.cleaned_data['password']) # Hash password
            user.save()
            messages.success(request, "Account created. Please log in.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render (request, 'store/register.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'store/profile.html', {'user': request.user})
        
@login_required
def account_orders(request):
    # fetch all orders for the logged-in user
    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    
    return render(request, 'store/account_orders.html', {
        'orders': orders
    })
    
@login_required
def sourcing(request):
    sizes_options = ["4", "4.5", "5", "5.5", "6", "6.5", "7", "7.5", "8", "8.5", "9", "9.5", "10"]
    
    if request.method == 'POST':
        form = SourcingRequestForm(request.POST)
        selected_sizes = request.POST.getlist('sizes[]')
        if not selected_sizes :
            messages.error(request, "Select size of sneaker to submit")
        elif len(selected_sizes) > 3:
            messages.error(request, "You can select a maximum of 3 sizes")
        elif form.is_valid():
            sourcing_request = form.save(commit = False)
            sourcing_request.user = request.user # Assign logged in user to request, so i can know who it is
            sourcing_request.sizes = ",".join(selected_sizes) # display size in comma in db
            sourcing_request.save() # Save to db
            messages.success(request, "Your sourcing request has been submitted.")
            return redirect("sourcing")
    else:
        form = SourcingRequestForm()
        
    return render(request, "store/sourcing.html", {
        "form": form,
        "sizes_options": sizes_options
        })

    
                
