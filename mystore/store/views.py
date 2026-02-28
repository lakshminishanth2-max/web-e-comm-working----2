from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login
from .models import *
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings

cart = []





def home(request):
    products = Product.objects.all()

    query = request.GET.get('q')
    category = request.GET.get('category')

    if query:
        products = products.filter(name__icontains=query)

    if category:
        products = products.filter(category__name=category)

    categories = Category.objects.all()

    return render(request, "home.html", {
        "products": products,
        "categories": categories
    })


def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, "product.html", {"product": product})


def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    cart.append(product)
    return redirect('/cart')


def cart_view(request):
    return render(request, "cart.html", {"cart": cart})


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('/')

    return render(request, "login.html")


def checkout(request):
    return render(request, "checkout.html")


def success(request):
    cart.clear()
    return render(request, "success.html")



@login_required
def add_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)

    Wishlist.objects.create(
        user=request.user,
        product=product
    )

    return redirect("home")


@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, "wishlist.html", {"items": items})

@login_required
def add_rating(request, product_id):
    if request.method == "POST":
        stars = request.POST['stars']
        review = request.POST['review']

        product = Product.objects.get(id=product_id)

        Rating.objects.create(
            user=request.user,
            product=product,
            stars=stars,
            review=review
        )

    return redirect("home")


@login_required
def place_order(request, product_id):

    product = Product.objects.get(id=product_id)

    order = Order.objects.create(
        user=request.user,
        total_price=product.price
    )

    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=1
    )

    return redirect("orders")

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders.html", {"orders": orders})

def payment(request, product_id):

    product = Product.objects.get(id=product_id)

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET)
    )

    payment = client.order.create({
        "amount": int(product.price * 100),
        "currency": "INR",
        "payment_capture": 1
    })

    return render(request, "payment.html", {
        "payment": payment,
        "product": product
    })