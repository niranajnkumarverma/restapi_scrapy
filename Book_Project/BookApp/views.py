from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.mail import send_mail
from random import randint
from django.conf import settings
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt

# API
from rest_framework.generics import ListAPIView
from .serializers import UserSerializer

class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
# Create your views here.

app_info = {
    'app_name': 'Book Store'
}

def index(request):
    products=Product.objects.all()
    wlist = [] #load_wishlist(request)
    cart = [] #load_cart(request)
    request.session['cart_total'] = 0
    request.session['app_name'] = 'Book Store'
    return render(request, 'index.html', {'products': products,'total_wlist': len(wlist), 'total_cart': len(cart)})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(Email=request.POST['email'], Password=request.POST['password'])
            request.session['email'] = request.POST['email']
            request.session['username'] = user.FullName
            request.session['status'] = user.IsActive
            request.session['pwd'] = user.Password
            request.session['address'] = user.Address
            request.session['mobile'] = user.Mobile
            
            if user.IsActive:
                if user.IsSeller:
                    request.session['type'] = 'seller'
                    products = view_product(request)
                    print(products)
                    return render(request, 'seller.html', {'products': products, 'total_products': len(products)})
                else:
                    request.session['type'] = 'customer'
                    products=Product.objects.all()
                    wlist = load_wishlist(request)
                    cart = load_cart(request)
                    return render(request, 'user.html', {'products': products, 'total_products': len(products), 'total_wlist': len(wlist), 'total_cart': len(cart)})
            else:
                send_otp_mail(request)
                msg = "Account status is inactive. please enter otp for activate account."
                return render(request, 'otp.html', {'msg': msg})
        except Exception as e:
            print(e)
            msg = "Invalid credentials. Please try again."
            return render(request, 'login.html', {'msg': msg})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        msg = ''
        try:
            user = User.objects.get(Email=request.POST['email'])
            if user:
                msg = "Already registered. Please login."
            return render(request, 'register.html', {'msg': msg})
        except Exception as e:
            print(e)
            User.objects.create(
                FullName=request.POST['fullname'],
                Email=request.POST['email'],
                Password=request.POST['password'],
                Mobile=request.POST['mobile'],
                IsSeller=request.POST['isseller'],
                Address=request.POST['address']
            )
        
            email_to = request.session['email'] = request.POST['email']
            
            send_otp_mail(request)
            
            msg = f"One Time Password has been sent to your {email_to}"

            return render(request, 'otp.html', {'otp':otp, 'email': email_to})
            #return render(request, 'register.html', {'msg': msg})
        
        return render(request, 'register.html', {'msg': msg})
    else:
        return render(request, 'register.html')

def send_otp_mail(request):
    email_to_list = [request.session['email'],]
    subject = 'OTP for Book Store Registration'
    otp = randint(1000,9999)
    print(otp)
    request.session['otp'] = otp
    message = f"Your One Time Password for Book Store Registration is: {otp}"
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, email_to_list)

def otp(request):
    if request.method == 'POST':
        if int(request.POST['otp']) == request.session['otp']:
            user = User.objects.get(Email=request.session['email'])
            user.IsActive = True
            user.save()
            del request.session['otp'],
            del request.session['email']
            #del request.session['username']
            msg = "Congratulations!! Your account successfully verified. Please login."
            return render(request, 'login.html', {'msg': msg})
        else:

            msg = "Your One Time Password does not matched. Please enter correct OTP."
            return render(request, 'otp.html', {'msg': msg})
    else:
        return render(request, 'otp.html')

def logout(request):
    if 'status' in request.session:
        del request.session['email']
        del request.session['status']
        del request.session['username']
        del request.session['pwd']
        del request.session['address']
        del request.session['mobile']

    return redirect(index)

def add_product(request):
    if request.method=="POST":
        Product.objects.create(
            product_seller=User.objects.get(Email=request.session['email']),
            product_name=request.POST['product_name'],
            product_author=request.POST['product_author'],
            product_price=request.POST['product_price'],
            product_desc=request.POST['product_desc'],
            product_image=request.FILES['product_image']
        )
        msg = "product added successfully."
        products = view_product(request)
        
        return render(request, 'seller.html', {'msg': msg, 'products': products, 'total_products': len(products)})
    else:
        return render(request, 'seller.html')

def add_product_page(request):
    products = view_product(request)
    print(products)
    return render(request, 'seller.html', {'products': products, 'total_products': len(products)})

def view_product(request):
	user=User.objects.get(Email=request.session['email'])
	products=Product.objects.filter(product_seller=user)
	return products

def user_view_product(request,bn):
    products=Product.objects.filter(product_name__contains=bn)
    wlist = load_wishlist(request)
    cart = load_cart(request)
    return render(request,'user_product_view.html',{'products':products, 'total_product': len(products), 'tag': bn,'wlist':wlist, 'cart': cart, 'total_wlist': len(wlist), 'total_cart': len(cart)})

def load_wishlist(request):
    user=User.objects.get(Email=request.session['email'])
    wishlists=WishList.objects.filter(user=user)
    request.session['total_wlist'] = len(wishlists)
    return wishlists

def load_cart(request):
    user=User.objects.get(Email=request.session['email'])
    cart=Cart.objects.filter(user=user)
    request.session['total_cart'] = len(cart)
    #print(cart)
    return cart

def user_product_detail(request,pk):
    wlist_flag=True
    cart_flag=True
    cart_qty = 0
    product=Product.objects.get(pk=pk)
    
    try:
        user=User.objects.get(Email=request.session['email'])
        wishlist=WishList.objects.get(product=product,user=user)
        if wishlist:
            wlist_flag=False
    except Exception as e:
        print(e)

    try:
        user=User.objects.get(Email=request.session['email'])
        cart=Cart.objects.get(product=product,user=user)
        if cart:
            cart_flag=False
            cart_qty = int(cart.qty)
    except Exception as e:
        print(e)
        
    wlist = load_wishlist(request)
    carts = load_cart(request)
    return render(request,'user_product_detail.html',{'product':product, 'cart_qty':cart_qty, 'wlist_flag': wlist_flag, 'cart_flag':cart_flag, 'wlist':wlist, 'carts': carts, 'total_wlist': len(wlist), 'total_cart': len(carts)})

def add_to_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(Email=request.session['email'])
	WishList.objects.create(product=product,user=user)
	return redirect('mywishlist')

def add_to_cart(request,pk):
    product=Product.objects.get(pk=pk)
    user=User.objects.get(Email=request.session['email'])
    Cart.objects.create(product=product,user=user,price=product.product_price,total=product.product_price)
    request.session['cart_total'] += product.product_price
    return redirect('mycart')

def mywishlist(request):
    user=User.objects.get(Email=request.session['email'])
    wishlists=WishList.objects.filter(user=user)
    cart = load_cart(request)
    wlist = load_wishlist(request)
    return render(request,'mywishlist.html',{'wishlists':wishlists, 'total_wlist': len(wishlists), 'total_cart': len(cart)})

def mycart(request):
    user=User.objects.get(Email=request.session['email'])
    cart=Cart.objects.filter(user=user)
    wlist = load_wishlist(request)
    carts = load_cart(request)
    total_cart_amt = 0
    for i in carts:
        total_cart_amt += int(i.total)
    return render(request,'mycart.html',{'cart':cart, 'cart_amt': total_cart_amt, 'total_wlist': len(wlist), 'total_cart': len(cart)})

def remove_from_wishlist(request,pk):
    product=Product.objects.get(pk=pk)
    user = User.objects.get(Email=request.session['email'])
    wishlist = WishList.objects.get(product=product, user=user)
    wishlist.delete()
    return redirect('mywishlist')

def remove_from_cart(request,pk):
    product=Product.objects.get(pk=pk)
    user = User.objects.get(Email=request.session['email'])
    cart = Cart.objects.get(product=product, user=user)
    cart.delete()
    return redirect('mycart')

def update_cart(request,pk):
    print(pk)
    product=Product.objects.get(pk=pk)
    user = User.objects.get(Email=request.session['email'])
    cart = Cart.objects.get(product=product, user=user)
    cart.qty = request.POST['qty']
    cart.price = product.product_price
    cart.total = int(request.POST['qty']) * product.product_price
    cart.save()
    return redirect('mycart')

def checkout(request):
    user=User.objects.get(Email=request.session['email'])
    cart=Cart.objects.filter(user=user)
    wlist = load_wishlist(request)
    cart = load_cart(request)
    return render(request,'checkout.html',{'cart':cart, 'total_wlist': len(wlist), 'total_cart': len(cart)})

def user_profile(request):
    return render(request,'user-profile.html')

def update_user(request):
    if request.method == 'POST':
        user=User.objects.get(Email=request.session['email'])
        
        #user.FullName=request.POST['fullname']
        #user.Email=request.POST['email']
        #user.Password=request.POST['password']
        #user.Mobile=request.POST['mobile']
        #user.Address=request.POST['address']

        user.FullName = request.session['username'] = request.POST['fullname']
        user.Email = request.session['email'] = request.POST['email']
        user.Password = request.session['pwd'] = request.POST['password']
        user.Mobile = request.session['mobile'] = request.POST['mobile']
        user.Address = request.session['address'] = request.POST['address']

        user.save()

        msg = 'Your profile updated successfully.'
        #return redirect(user_profile)
        return render(request, 'user-profile.html', {'msg': msg})
    else:
        return render(request,'user-profile.html')

def product_detail(request, pk):
	user=User.objects.get(Email=request.session['email'])
	product=Product.objects.get(product_seller=user,pk=pk)
	return render(request,'product_details.html',{'products':product})

def product_edit(request,pk):
	user=User.objects.get(Email=request.session['email'])
	product=Product.objects.get(product_seller=user,pk=pk)
	if request.method=="POST":

		product.product_name=request.POST['product_name']
		product.product_price=request.POST['product_price']
		product.product_author=request.POST['product_author']
		product.product_desc=request.POST['product_desc']
		try:
			product.product_image=request.FILES['product_image']
		except:
			pass
		product.save()
		product=Product.objects.get(product_seller=user,pk=pk)
		return render(request,'product_details.html',{'products':product, 'msg': f"{product.product_name} is updated successfully."})

	else:
		return render(request,'product_edit.html',{'products':product})

def product_delete(request, pk):
	user=User.objects.get(Email=request.session['email'])
	product=Product.objects.get(product_seller=user, pk=pk)
	product.delete()
    #products = view_product(request)
	return render(request,'seller.html',{'products':view_product(request), 'total_products': len(view_product(request))})

## payment views
def initiate_payment(request):
    try:
        user=User.objects.get(Email=request.session['email'])
        amount = int(request.POST['net_price'])
    except Exception as e:
        print(e)
        return render(request, 'mycart.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.Email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://localhost:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
            msg = 'Your payment made successfully done.'
        else:
            msg = 'Your payment failed. Please try again later.'
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        #return render(request, 'mycart.html', context=received_data)
        return redirect('mycart')