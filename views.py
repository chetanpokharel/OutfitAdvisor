from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.conf import settings
import pickle
import numpy as np
from numpy.linalg import norm
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from sklearn.neighbors import NearestNeighbors
from tensorflow.keras.preprocessing import image
from tensorflow.keras import Sequential
from tensorflow.keras.layers import GlobalMaxPooling2D
import os
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from .models import Cart, Product
from phonenumber_field.formfields import PhoneNumberField
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.shortcuts import render
from .models import CartItem
from django.http import JsonResponse
from .models import Cart

def add_to_cart(request):
    if request.method == "POST":
        product_name = request.POST.get('product_name')
        if product_name:
            cart_item, created = CartItem.objects.get_or_create(product_name=product_name)
            if not created:
                cart_item.quantity += 1  
            cart_item.save()

            cart_count = CartItem.objects.count()

            return JsonResponse({"success": True, "cart_count": cart_count})
        else:
            return JsonResponse({"success": False, "error": "Invalid product"})
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

def cart_view(request):
    cart_items = CartItem.objects.all()
    return render(request, "app/cart.html", {"cart_items": cart_items})

def update_cart(request):
    if request.method == 'POST':
        item_id = request.POST['item_id']
        quantity = int(request.POST['quantity'])

        # Get the cart item by its ID and update the quantity
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.quantity = quantity
        cart_item.save()

        # Recalculate the total amount for the cart and generate item names
        total_amount = sum(item.price * item.quantity for item in CartItem.objects.filter(user=request.user))
        item_names = ", ".join([item.product_name for item in CartItem.objects.filter(user=request.user)])

        # Generate updated cart HTML to send back
        cart_html = render_to_string('cart_items.html', {'cart_items': CartItem.objects.filter(user=request.user)})

        return JsonResponse({
            'cart_html': cart_html,
            'total_amount': total_amount,
            'item_names': item_names,
        })


def remove_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        try:
            item = CartItem.objects.get(id=item_id)
            item.delete()  # Remove the item from the cart
        except CartItem.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status=404)

        # Retrieve updated cart items and calculate total
        cart_items = CartItem.objects.all()
        total_amount = sum(item.price * item.quantity for item in cart_items)
        item_names = ', '.join([item.product_name for item in cart_items])

        # Return the updated cart HTML and total amount as part of the response
        cart_html = render_to_string('app/cart_items.html', {'cart_items': cart_items})
        return JsonResponse({
            'cart_html': cart_html,
            'total_amount': total_amount,
            'item_names': item_names
        })
    return JsonResponse({"error": "Invalid request"}, status=400)

def home(request):
    return render(request, 'app/home.html')

def product_detail(request):
    return render(request, 'app/productdetail.html')

def check_login_status(request):
    return JsonResponse({'is_logged_in': request.user.is_authenticated})

def profile_page(request):
    # Check if the user is logged in
    if not request.user.is_authenticated:
        # Clear the cart if the user is not logged in
        Cart.objects.filter(user=None).delete()  # Or clear any cart data as needed

    # Add any other profile page context here
    return render(request, 'app/profile.html')

def buy_now(request):
    return render(request, 'app/buynow.html')

def address(request):
    return render(request, 'app/address.html')

def change_password(request):
    return render(request, 'app/changepassword.html')

def mobile(request):
    return render(request, 'app/mobile.html')

def logout_view(request):
    logout(request)  # Logs out the user and ends the session
    return redirect('home,html')  # Redirect to the home page or wherever you want # Replace 'home' with your desired redirect URL after logout

@login_required(login_url='login')  # Redirects to login if the user is not authenticated
def place_order(request):
     # Logic to display the place order page
    cart_items = Cart.objects.filter(user=request.user, is_ordered=False)

    # If the cart is empty, redirect the user back to the cart page
    if not cart_items.exists():
        return redirect('cart.html')  # Assuming you have a 'cart' page

    return render(request, 'app/place_order.html', {'cart_items': cart_items})

def Cus_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Get the cleaned data
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            
            # Manually hash the password
            hashed_password = make_password(password)

            # Create the user with hashed password
            user = User.objects.create_user(
                username=username,
                email=email,
                password=hashed_password
            )
            
            # Optionally, you can authenticate the user here and log them in
            user = authenticate(username=username, password=password)  # Authenticate with raw password (not hashed)
            if user is not None:
                login(request, user)

            # Redirect to the login page after successful registration
            return redirect('login')  # Make sure 'login' is the correct path name
    else:
        form = RegisterForm()
    
    return render(request, 'app/Cus_register.html', {'form': form})

def test_auth(request):
    if request.user.is_authenticated:
        return HttpResponse(f"User {request.user.username} is logged in.")
    else:
        return HttpResponse("User is not logged in.")

def some_protected_view(request):
    return render(request, 'app/protected.html')

def checkout(request):
    cart_items = CartItem.objects.all()

    # Calculate total price
    #total_price = sum(item.price * item.quantity for item in cart_items)

    # Collect item names (product image names in JPG format)
    item_names = [item.product_name for item in cart_items] 

    delivery_hub = {
        "name": "Delivery Hub",
        "address": "Main Street, City Center",
        "location": "Kathmandu, Nepal"
         }   
    if request.method == "POST":
        return redirect('home')  # Redirect after checkout

    return render(request, 'app/checkout.html', {
        'cart_items': cart_items,
        #'total_price': total_price,
        'item_names': item_names,
        'delivery_hub': delivery_hub,
    })

def order_summary(request):
    user = request.user
    if user.is_authenticated:
        # Clear the cart when checking the order summary
        Cart.objects.filter(user=user).delete()  

    # Retrieve the items and total from the request's query parameters
    items = request.GET.get('items', '')
    quantities = request.GET.get('quantities', '')
    total_price = request.GET.get('total', '')

    # Ensure that we have items, quantities, and total in the URL
    if not items or not total_price:
        error_message = "Missing order details"
        return render(request, 'app/orders.html', {'error': error_message})

    items_list = items.split(', ')
    quantities_list = quantities.split(', ') if quantities else []
    
    # If quantities aren't passed, assume each item has quantity 1
    if not quantities_list:
        quantities_list = ['1'] * len(items_list)

    context = {
        'items': items_list,
        'quantities': quantities_list,
        'total_price': total_price,
    }

    return render(request, 'app/orders.html', context)

def clear_cart(request):
    if request.method == "POST":
        # Get the current user (modify if using session-based cart)
        user = request.user if request.user.is_authenticated else None

        # Delete all cart items related to the user
        Cart.objects.filter(user=user).delete()

        return JsonResponse({"message": "Cart cleared successfully!"})
    return JsonResponse({"error": "Invalid request"}, status=400)

def index(request):
    if request.method == "POST" and request.FILES.get('upload'):
        upload = request.FILES['upload']
        return render(request, 'base.html', {'message': 'Image uploaded successfully'})

def fetch(request):
    if request.method == "POST":
        if 'upload' not in request.FILES:
            err = 'No images Selected'
            return render(request, './app/final.html', {'err': err})

        upload = request.FILES['upload']
        filename = upload.name
        with default_storage.open(filename, 'wb+') as destination:
            for chunk in upload.chunks():
                destination.write(chunk)

        # Fixing the pickle file loading
        try:
            feature_list = np.array(pickle.load(open('./shoppinglyx/embeddings.pkl', 'rb')))
            filenames = pickle.load(open('./shoppinglyx/filenames.pkl', 'rb'))
        except Exception as e:
            return render(request, './app/final.html', {'err': f"Error loading pickle files: {e}"})

        model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        model.trainable = False
        model = Sequential([model, GlobalMaxPooling2D()])

        # Process the uploaded image
        img = image.load_img(os.path.realpath(destination.name), target_size=(224, 224))
        img_array = image.img_to_array(img)
        expanded_img_array = np.expand_dims(img_array, axis=0)
        preprocessed_img = preprocess_input(expanded_img_array)
        result = model.predict(preprocessed_img).flatten()
        normalized_result = result / norm(result)

        # Find similar images using Nearest Neighbors
        neighbors = NearestNeighbors(n_neighbors=6, algorithm='brute', metric='euclidean')
        neighbors.fit(feature_list)
        distances, indices = neighbors.kneighbors([normalized_result])

        result_urls = []
        for file in indices[0][0:5]:
            image_name = filenames[file].split("/")[-1]
            result_urls.append(image_name)

        uploaded_image_url = f"{settings.MEDIA_URL}{filename}"

        return render(request, './app/final.html', {'context': result_urls, 'uploaded_image_url': uploaded_image_url})

def final(request):
    return render(request, './app/final.html')


