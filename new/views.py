from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from .models import Product,category,SubCategory
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect(login)

    return render(request, "register.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("index")
        else:
            messages.error(request, "Invalid username or password!")
            return redirect("login")

    return render(request, "login.html")

def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect(index)

def search(request):
    query = request.GET.get('search', '')  # Get the search query from the request
    if query:
        post = Product.objects.filter(
            Q(name__icontains=query) 
        )

    else:
        post = Product.objects.all()  # Fetch all students if no query
    
    cart = request.session.get('cart', {}) or {}
    categories=category.objects.all()

    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        try:
            price = int(float(item['price']))  # Convert price to float first, then int
            quantity = int(item['quantity'])  # Convert quantity to integer
        except (ValueError, TypeError):
            price = 0
            quantity = 0

        item_total = price * quantity  # Multiply price * quantity
        total_price += item_total  # Add to total cart price

        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'price': price,
            'image': item.get('image', 'default_image.jpg'),  # Use default if missing
            'quantity': quantity,
            'total': item_total,  # Store subtotal
        })

    context = {
        'post': post,
        'categories':categories,
        'cart_items': cart_items,
        'cart_count': len(cart),
        'total_price': total_price,  # Pass total cart price
    }

    return render(request, 'index.html', context)

# Create your views here.
def index(request):
    post = Product.objects.all()
    categories=category.objects.all()
    subcategory=SubCategory.objects.all()
    cart = request.session.get('cart', {}) or {}

    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        try:
            price = int(float(item['price']))  # Convert price to float first, then int
            quantity = int(item['quantity'])  # Convert quantity to integer
        except (ValueError, TypeError):
            price = 0
            quantity = 0

        item_total = price * quantity  # Multiply price * quantity
        total_price += item_total  # Add to total cart price

        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'price': price,
            'image': item.get('image', 'default_image.jpg'),  # Use default if missing
            'quantity': quantity,
            'total': item_total,  # Store subtotal
        })

    context = {
        'post': post,
        'categories':categories,
        'subcategory':subcategory,
        'cart_items': cart_items,
        'cart_count': len(cart),
        'total_price': total_price,  # Pass total cart price
    }

    return render(request, 'index.html', context)

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if category.has_subcategories:
        # If category has subcategories, display message or empty page
        products = None
    else:
        # Show products directly linked to the category
        products = Product.objects.filter(category=category)

    return render(request, 'category_products.html', {'category': category, 'products': products})

def subcategory_products(request, slug):
    subcategory = get_object_or_404(SubCategory, slug=slug)
    products = Product.objects.filter(subcategory=subcategory)
    return render(request, 'subcategory_products.html', {'subcategory': subcategory, 'products': products})

@login_required(login_url=user_login)
def addproduct(request):
    if request.method == 'POST':
        p=Product()
        p.name=request.POST.get('name')
        p.price=request.POST.get('price')
        p.detail=request.POST.get('detail')
        ca=request.POST.get('category')
        categorys=get_object_or_404(category,pk=ca)
        p.category=categorys
        p.image=request.FILES.get('image')
        p.save()
        return redirect(index)
    else:
        cat=category.objects.all()
        return render(request,'addproduct.html',{'cat':cat})

@login_required(login_url=user_login)
def showproduct(request):
    products=Product.objects.all()
    return render(request,'showproduct.html',{'products':products})

@login_required(login_url=user_login)
def editproduct(request,pk):
    p=get_object_or_404(Product,pk=pk)
    if request.method == 'POST':
        p.name=request.POST.get('name')
        p.price=request.POST.get('price')
        p.detail=request.POST.get('detail')
        if request.FILES.get('image'):
            p.image = request.FILES.get('image')
        p.save()
        return redirect(showproduct)
    else:
        products=product.objects.all()
        return render(request,'editproduct.html',{'p':p,'products':products})

@login_required(login_url=user_login)
def deleteproduct(request,pk):
    p=get_object_or_404(Product,pk=pk)
    p.delete()
    return redirect(showproduct)

@login_required(login_url=user_login)
def addcategory(request):
    if request.method == 'POST':
        c = category()  # Ensure the correct model name
        c.name = request.POST.get('name')
        c.detail = request.POST.get('detail')
        c.slug = request.POST.get('slug')
        c.has_subcategories = 'has_subcategories' in request.POST  # Checkbox handling
        c.save()
        return redirect('showcategory')  # Use name if defined in `urls.py`
    
    return render(request, 'addcategory.html')

@login_required(login_url=user_login)   
def showcategory(request):
    categories=category.objects.all()
    sub=SubCategory.objects.all()
    return render(request,'showcategory.html',{'categories':categories,'sub':sub})

@login_required(login_url=user_login)
def editcategory(request,pk):
    c=get_object_or_404(category,pk=pk)
    if request.method == 'POST':
        c.name=request.POST.get('name')
        c.detail=request.POST.get('detail')
        c.save()
        return redirect(showcategory)
    else:
        categories=category.objects.all()
        return render(request,'editcategory.html',{'c':c,'category':category})

@login_required(login_url=user_login)   
def deletecategory(request,pk):
    p=get_object_or_404(category,pk=pk)
    p.delete()
    return redirect(showcategory)

def addsubcategory(request):
    if request.method =='POST':
        s=SubCategory()
        ca=request.POST.get('category')
        categorys=get_object_or_404(category,pk=ca)
        s.category=categorys
        s.name=request.POST.get('name')
        s.slug=request.POST.get('slug')
        s.save()
        return redirect(showcategory)
    else:
        cat=category.objects.all()
        return render(request,'addsubcategory.html',{'cat':cat})
        
        

def viewproduct(request,pk):
    p = get_object_or_404(Product,pk=pk)
    categories=category.objects.all()
    cart = request.session.get('cart', {}) or {}

    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        try:
            price = int(float(item['price']))  # Convert price to float first, then int
            quantity = int(item['quantity'])  # Convert quantity to integer
        except (ValueError, TypeError):
            price = 0
            quantity = 0

        item_total = price * quantity  # Multiply price * quantity
        total_price += item_total  # Add to total cart price

        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'price': price,
            'image': item.get('image', 'default_image.jpg'),  # Use default if missing
            'quantity': quantity,
            'total': item_total,  # Store subtotal
        })

    context = {
        'p': p,
        'categories':categories,
        'cart_items': cart_items,
        'cart_count': len(cart),
        'total_price': total_price,  # Pass total cart price
    }

    return render(request, 'viewproduct.html', context)

def addtocart(request, pk):
    """Add product to the session-based cart"""
    cart = request.session.get('cart', {})

    # Add product to cart or increase quantity
    if str(pk) in cart:
        cart[str(pk)]['quantity'] += 1
    else:
        product = get_object_or_404(Product, id=pk)
        cart[str(pk)] = {
            'name': product.name,
            'price': int(product.price),
            'image': product.image.url,
            'quantity': 1,
        }

    request.session['cart'] = cart

    # Stay on search page if coming from search, otherwise redirect to index
    referer_url = request.META.get('HTTP_REFERER', '')

    if 'search' in referer_url:
        return redirect(referer_url)  # Stay on search page
    else:
        return redirect("index")
   

@login_required(login_url=user_login)
def adminhome(request):
    product_count = Product.objects.count()
    category_count = category.objects.count()

    recent_products = Product.objects.order_by('-id')[:5]

    context = {
        'product_count': product_count,
        'category_count': category_count,
        'recent_products': recent_products,
    }
    return render(request, 'adminhome.html', context)

def cart_detail(request):
    """Display the cart details"""
    cart = request.session.get('cart', {})
    return render(request, 'cart_detail.html', {'cart': cart})

def remove_from_cart(request, product_id):
    """Remove a product from the cart"""
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('index')

def productcategory(request, category_id):  # Ensure category_id is correctly passed
    categorys = get_object_or_404(category, id=category_id)  # Get category
    post = Product.objects.filter(category=categorys)  # Get products in category
    categories = category.objects.all()  # Fetch all categories for sidebar
    cart = request.session.get('cart', {}) or {}
    
    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        try:
            price = int(float(item['price']))  # Convert price to float first, then int
            quantity = int(item['quantity'])  # Convert quantity to integer
        except (ValueError, TypeError):
            price = 0
            quantity = 0

        item_total = price * quantity  # Multiply price * quantity
        total_price += item_total  # Add to total cart price

        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'price': price,
            'image': item.get('image', 'default_image.jpg'),  # Use default if missing
            'quantity': quantity,
            'total': item_total,  # Store subtotal
        })

    context = {
        'post': post,
        'categories': categories,
        'categorys': categorys,
        'cart_items': cart_items,
        'cart_count': len(cart),
        'total_price': total_price, 
    }
    return render(request, 'productcategory.html', context)

@login_required(login_url=user_login)
def chechout(request):
    return render(request,'checkout.html')
