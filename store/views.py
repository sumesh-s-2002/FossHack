from xmlrpc import client
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse,HttpResponseBadRequest
from django.contrib.auth.forms import UserCreationForm
from . import forms,models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login as auth_login, logout as logout_view
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from uuid import uuid4
from django.core.mail import send_mail
import razorpay
from django.views.decorators.csrf import csrf_exempt
from ecommerse.settings import RAZOR_KEY_ID, RAZOR_KEY_SECRET

#creating razorpay client
razorpay_client = razorpay.Client(auth=(RAZOR_KEY_ID,RAZOR_KEY_SECRET)) 

def home(request):
    featured = models.Collection.objects.first().product.all()
    latest = models.Collection.objects.last().product.all()
    title1 = models.Collection.objects.first().title
    title2 = models.Collection.objects.last().title
    context  = {"featured" : featured, "latest" : latest, "title1" : title1, "title2" : title2}
    return render(request, 'store/home.html', context)

def contacts(request):
    if request.method == 'POST':
        name = request.POST["name"]
        email = request.POST["email"]
        message = request.POST["message"]
        send_mail("mail from " + name,
        message, "dreamflowers639@gmail.com" ,["dreamflowers639@gmail.com"], fail_silently=True)
        return redirect("Home-page")
    return render(request, 'store/contacts.html')
def products(request):
    if "form-data" in request.GET:
        form_data = request.GET['form-data']
        productspag = models.Product.objects.filter(title__icontains = form_data)
    else:  
        productspag = models.Product.objects.all()
    page = request.GET.get('page', 1)
    p = Paginator(productspag, per_page=10)
    try :
        products = p.page(page)
    except PageNotAnInteger:
        products = p.page(1)
    except EmptyPage:
        products = p.page(p.num_pages)
    context = {"products" : products}
    return render(request, 'store/products.html', context)

@login_required(login_url='Login-page')
def cart(request):
    customer = request.user.customer
    cart = models.Cart.objects.get(customer=customer)
    cartItems = cart.cartitem_set.all()
    count = cartItems.count()
    context = {"cartitems" : cartItems, "count" : count, "cart" : cart}
    return render(request, 'store/cart.html', context)

def logout(request):
    logout_view(request)    
    return redirect("Home-page")

def login(request):
    if request.method == "POST" :
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("Home-page")
        else:
            messages.error(request, "username or password is incorrect")
    return render(request, 'store/login.html')

def register(request):
    if request.method == "POST":
        form = forms.RegitrationForm(request.POST)
        if(form.is_valid()):
            user = form.save()
            models.Customer.objects.create(user=user)
            messages.success(request, str(request.user.username)+" created succesfully")
            email =  user.email
            send_mail("hellow"+ str(user), "Thank you for registering to Xstores! explore our store by just clicking on this link http://127.0.0.1:8000/products/","dreamflowers639@gmail", [email], fail_silently=True)
            return redirect("Login-page")
    else:
       form = forms.RegitrationForm()
    context = {"form" : form}
    return render(request, 'store/register.html', context)

def myprofile(request):
    customer = request.user.customer
    try:
        orders = models.Order.objects.filter(customer=customer)
        orderitems = []
        for order in orders:
            orderitem = models.OrderItem.objects.filter(order = order)
            orderitems.append(orderitem)
    except ObjectDoesNotExist:
        orders = []
    if request.method == "POST":
        form1 = forms.UserForm(request.POST,instance=request.user)
        form2 = forms.CustomerForm(request.POST,request.FILES,instance=customer)
        if(form1.is_valid() & form2.is_valid()):
            form1.save()
            form2.save()
            return redirect("Myprofile-page")
    else:
        form1 = forms.UserForm(instance=request.user)
        form2 = forms.CustomerForm(instance=customer)
    context = {"customer" : customer, "form1" : form1 , "form2" : form2, "orderitems" : orderitems}
    return render(request, 'store/myprofile.html', context)

@login_required(login_url='Login-page')
def checkout(request):
    customer = request.user.customer
    cart = models.Cart.objects.get(customer=customer)
    cartItems = cart.cartitem_set.all()
    count = cartItems.count()
    userform = forms.UserForm(instance=request.user)
    #address form validation
    if request.method == "POST":
        addressform = forms.AddressForm(request.POST)
        if not addressform.is_valid():
            add = addressform.cleaned_data["address"]
            city = addressform.cleaned_data["city"]
            state = addressform.cleaned_data["state"]
            zip = addressform.cleaned_data["zip"]
            addressget, creates = models.Address.objects.get_or_create(address=add, city=city, state=state, zip=zip, customer=customer)
            orderid = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
            order, created = models.Order.objects.get_or_create(address=addressget, customer=customer, reference=orderid)
            for cartitem in cartItems:
                models.OrderItem.objects.create(order=order, product=cartitem.product, quantity=cartitem.quantity, unit_price=cartitem.product.price)
            return redirect("payment-page")
    else:
        try:
            address = models.Address.objects.filter(customer=customer).first()
            addressform = forms.AddressForm(instance=address)
        except ObjectDoesNotExist:
            addressform = forms.AddressForm()
    context = {
        "count" : count, "cartitems" : cartItems, "cart" : cart, "userform" : userform, "addressform" : addressform
    }
    return render(request, 'store/checkout.html', context)

@login_required(login_url='Login-page')
def addToCart(request):
    customer = request.user.customer
    data = json.loads(request.body)
    id = data['id']
    action = data['action']
    product = models.Product.objects.get(id=id)
    cart, created = models.Cart.objects.get_or_create(customer=customer)
    cartitem , created1 = models.CartItem.objects.get_or_create(cart=cart, product=product)
    if(action == "add"):
        cartitem.quantity += 1
    elif(action == "remove"):
        cartitem.quantity -= 1

    cartitem.save()
    print(cartitem.quantity)
        
    return JsonResponse("hellow", safe=False)

@login_required(login_url='Login-page')
def updateCart(request):
    data = json.loads(request.body)
    id = data["id"]
    value = int(data['value'])
    customer = request.user.customer
    cart = models.Cart.objects.get(customer=customer)
    cartitem = cart.cartitem_set.get(id=id)
    if(value <= 0):
        cartitem.delete()
    else:
        cartitem.quantity = value
        cartitem.save()
    
    return JsonResponse("hellow", safe=False)

def productDetails(request, id):
    product = models.Product.objects.get(id=id)
    images_list = []
    try:
        images = models.ProductImages.objects.get(product=product)
        images_list.append(images.image0.url)
        images_list.append(images.image1.url)
        images_list.append(images.image2.url)
        images_list.append(images.image3.url)
    except ObjectDoesNotExist:
        images_list = []
    context = {"product" : product, "images" : images_list, "id" : id}
    return render(request, 'store/product-details.html', context)

@login_required
def payment(request):
    customer = request.user.customer
    customer1 = models.Customer.objects.get(user = request.user)
    cart = models.Cart.objects.get(customer=customer)
    amount = int(cart.grandTotal)*100
    currency = "INR"
    key = RAZOR_KEY_ID
    callback_url = "paymenthandler/"
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
    razorpay_id = razorpay_order["id"]
    order = models.Order.objects.filter(customer = customer).last()
    order.razorpay_order_id = razorpay_id
    order.save()
    context = {"key" : key, "amount" : amount, "currency" : currency, "callback_url" : callback_url, "id" : razorpay_id,"customer" : customer1}
    return render(request, "store/payment.html",context)

@csrf_exempt
def paymentHandler(request):
    customer = request.user.customer
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            print(payment_id, razorpay_order_id, signature)
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            order = models.Order.objects.filter(customer = customer).last()
            order.razorpay_payment_id = payment_id
            order.razorpay_signature = signature
            order.save()
            cart = models.Cart.objects.get(customer=customer)
            cartitem = cart.cartitem_set.all()
            for item in cartitem:
                item.delete()
            status = razorpay_client.utility.verify_payment_signature(params_dict)
            if(status):
                order.payment_status = "S"
                order.save()
            return render(request, "store/summary.html", {"status" : status})
        except:
            return render(request, "store/summary.html", {"status" : "payment failuer"})
    else:
        return HttpResponseBadRequest()