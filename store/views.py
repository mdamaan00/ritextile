from django.contrib import auth
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.urls import reverse
from .Paytm import checksum
from .models import *
from .filters import ItemFilter
import json
import datetime
import stripe
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:

        items = []
        order = {'get_cart_total':0,'get_cart_item':0,'shipping': False}
        cartItems = order['get_cart_item']
    products = Product.objects.all()
    productsSaree = Product.objects.filter(category=1)
    productsDupatta = Product.objects.filter(category=2)
    productsSuits = Product.objects.filter(category=3)
    categories = Categories.objects.all()
    context = {'cartItems':cartItems,'categories':categories,'productsSaree':productsSaree[::-1],
    'productsDupatta':productsDupatta[::-1],'productsSuits':productsSuits[::-1],'products':products[::-1]}
    return render(request,'store/home.html',context)
@login_required(login_url='login')
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_item':0,'shipping': False}
        cartItems = order['get_cart_item']
        
    categories = Categories.objects.all()
    total = order.get_cart_total
    tax = (5*total)/100
    grandTotal = tax + total
    context = {'items':items , 'order':order,'cartItems':cartItems,'categories':categories,'grandTotal':grandTotal,'tax':tax}
    return render(request,'store/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_item':0,'shipping': False}
        cartItems = order['get_cart_item']
    if not cartItems:
        return redirect('cart')
    
    if request.is_ajax():
        address = ShippingAddress.objects.get(id=request.POST.get("id"),customer=customer)
        address.delete()
        return JsonResponse({'msg':"SUCCESS"})


    if request.POST.get('first_name') :
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        phonenumber =request.POST.get('phonenumber')
        ShippingAddress.objects.create(
            customer=customer,
            first_name=first_name,
            last_name=last_name,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            phonenumber=phonenumber
        )
        mainaddress = ShippingAddress.objects.filter(customer=customer)
        mainaddress = mainaddress[len(mainaddress)-1]
        AllAddresses.objects.create(
            customer=customer,
            first_name=first_name,
            last_name=last_name,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            phonenumber=phonenumber,
            mainaddressmodel=mainaddress
        )
        return redirect(request.path)
    categories = Categories.objects.all() 
    address = ShippingAddress.objects.filter(customer=customer)   
    total = order.get_cart_total
    tax = (5*total)/100
    grandTotal = tax + total
    print(order.get_cart_item)
    context = {'items':items , 'order':order,'cartItems':cartItems,'categories':categories,'address':address,'tax':tax,'grandTotal':grandTotal}
    return render(request,'store/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:',action)
    print('ProductId:',productId)
    product = Product.objects.get(id=productId)
    customer = request.user  
    order, created = Order.objects.get_or_create(customer=customer , complete=False)
    orderItem, created = OrderItem.objects.get_or_create(customer=customer,order=order,product=product)
    if action == "add":
        orderItem.quantity +=1
    elif action == "remove":
        orderItem.quantity-=1
    orderItem.save()
    if orderItem.quantity<=0 or action=="delete":
        orderItem.delete()
        
    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    if request.method=="POST":
        data = request.POST.get('groupOfDefaultRadios')
        if request.POST.get('payment')=="cod":
            return redirect('checkout')
        # transaction_id = datetime.datetime.now().timestamp()
        # data = json.loads(request.body)
        if request.user.is_authenticated:
            customer = request.user
            order, created = Order.objects.get_or_create(customer=customer , complete=False)
            if order.get_cart_item<=0:
                return redirect('checkout')
            # order.transaction_id = transaction_id
            tax = (5*order.get_cart_total)/100
            grandTotal = tax + order.get_cart_total
            # order.total = order.get_cart_total
            # order.tax = tax
            # order.grandtotal = grandTotal
            # order.complete = True
            # order.status = 'Order Processing'
            # order.save()
            # items = order.orderitem_set.all()
            # for item in items:
            #     prod = Product.objects.get(id=item.product.id)
            #     item.sp = item.get_total
            #     item.save()
            #     prod.stock -= item.quantity
            #     if prod.stock<=0:
            #         prod.available = False
            #     prod.save()
            # request.session['prod_id']=order.id
            # request.session['address_id']=data
            # request.session['customer_id']= request.user.id
            # request.session['transaction_id']=transaction_id
            # request.session['custom_url'] = int(data['customurl'])
            if order.shipping == True:
                shippingaddress=ShippingAddress.objects.get(id=int(data))
                address = AllAddresses.objects.get(mainaddressmodel=shippingaddress)
                order.address = address
                order.date_orderd = datetime.date.today()
            order.save()
            params = {
             'MID':'GJrYCg15603646443443',
             'ORDER_ID':str(order.id),
             'TXN_AMOUNT': str(grandTotal),
             'CUST_ID': str(request.user.id),
             'INDUSTRY_TYPE_ID':'Retail',
             'WEBSITE':'WEBSTAGING',
             'CHANNEL_ID':'WEB',
             'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',
                
            }
            #http://ritextiles-test-2.herokuapp.com/
            params['CHECKSUMHASH'] = checksum.generate_checksum(param_dict=params,merchant_key= "ke3Q@9&y8857%kZ&")
            request.session['params'] = json.dumps(params)
            return redirect('paytm')
        else:
            print('User is not logged in...')
    else:
        return HttpResponse("ERROR")

    return JsonResponse('Payment Complete!', safe=False)
    

def paytm(request):
    params = request.session['params']
    del request.session['params']
    params = json.loads(params)
    return render(request, 'store/paytm.html',{'params':params})


def search(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_item':0,'shipping': False}
        cartItems = order['get_cart_item']
    query = request.GET.get('search')
    if query:
        productsName = Product.objects.filter(name__icontains=query)
        productsDescription = Product.objects.filter(description__icontains=query)
        productsPrice = Product.objects.filter(price__icontains=query)
        products = productsName.union(productsDescription,productsPrice)
    else:
        products = None

    categories = Categories.objects.all()
    context={'cartItems':cartItems,'categories':categories,'query':query,'products':products}
    return render(request,'store/search.html',context)


def loginPage(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')
                return redirect('login')
        else:
            items = []
            order = {'get_cart_total':0,'get_cart_item':0,'shipping': False}
            cartItems = order['get_cart_item']
            categories = Categories.objects.all()
            context = {'cartItems':cartItems,'categories':categories}
            return render(request,'store/login.html',context)
    else:
        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        return HttpResponse("You are already logged in")


def registerPage(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email = request.POST.get('email')
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if User.objects.filter(email=email):
                messages.error(request,"E-mail id already exists" )
                return redirect('register')
            if password1!=password2:
                messages.error(request,"Passwords you entered didn't match" )
                return redirect('register')
            user = User.objects.create_user(email=email, password=password1)
            user.first_name = fname
            user.last_name = lname
            user.save()
            login(request, user)
            return redirect('home')
        else:
            items = []
            order = {'get_cart_total':0,'get_cart_item':0,'shipping': False}
            cartItems = order['get_cart_item']
            categories = Categories.objects.all()
            context = {'cartItems':cartItems,'categories':categories}
            return render(request,'store/register.html',context)
    else:
        return HttpResponse('404- Page not found')

def logoutUser(request):
    logout(request)
    return redirect('home')

def products(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_item':0,'shipping': False}
        cartItems = order['get_cart_item']
    products = Product.objects.all()
    materials = Material.objects.all()
    categories = Categories.objects.all()

    myfilter = ItemFilter(request.GET,queryset= products)
    products = Paginator(myfilter.qs,6)
    
    page_number = request.GET.get("page")
    products_page_obj = products.get_page(page_number)
    context = {'products':products,'cartItems':cartItems,'materials':materials,
    'categories':categories , 'myfilter':myfilter,"products_page_obj":products_page_obj}
    return render(request, 'store/products.html',context)

@login_required(login_url='login')
def profile(request):
    customer = request.user
    orders = Order.objects.filter(customer=customer,complete=True)[::-1]
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_item':0,'shipping': False}
        cartItems = order['get_cart_item']
    
    categories = Categories.objects.all()
    context = {'items':items, 'cartItems':cartItems,'categories':categories,'orders':orders,'customer':customer}

    return render(request, 'store/userpage.html',context)

def productsView(request,myid):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_item':0,'shipping': False}
        cartItems = order['get_cart_item']
    product = Product.objects.get(id=myid)
    if request.is_ajax():
        if request.POST.get('id'):
            reviews = Reviews.objects.get(id = request.POST.get('id'),customer = request.user)
            reviews.delete()
            messages.success(request,'Your review has been deleted successfully.')
            return JsonResponse({'msg':'Deleted'})
        if request.POST.get('quantity'):
            quantity = request.POST.get('quantity')
            quantity = int(quantity)
            print(product)
            print(quantity)
            orderItem,created = OrderItem.objects.get_or_create(customer=customer,order=order,product=product)
            if quantity>=1 and (quantity<=(5-orderItem.quantity) and quantity<=orderItem.product.stock-orderItem.quantity):
                orderItem.quantity+=quantity
                orderItem.save()   
                allItems = order.get_cart_item
                return JsonResponse({"item":allItems,'quantity':quantity})
            elif quantity>orderItem.product.stock-orderItem.quantity:
                #product out of stock
                return JsonResponse({'quan1':orderItem.product.stock})
            elif quantity>(5-orderItem.quantity):
                #off cart limit
                return JsonResponse({'quan':1})
            elif orderItem.quantity<=0:
                orderItem.delete()

    if request.POST.get('comments'):
        comments = request.POST.get('comments')
        rating = request.POST.get('rating')
        if rating:
            review = Reviews.objects.create(customer=customer,product=product,comment=comments,rating=rating)
            review.save()
            messages.success(request,'Your review has been sent. Thanks for your interest.')
        else:
            messages.error(request,'Please give a valid rating')
        return redirect(request.path)
    reviews = Reviews.objects.filter(product=product)
    images = Images.objects.filter(product=product)
    categories = Categories.objects.all()
    context={'product':product,'images':images,'cartItems':cartItems,'reviews':reviews[::-1],'categories':categories}
    return render(request,'store/productsview.html',context)

def changePassword(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PasswordChangeForm(user=request.user,data = request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Your Password has been changed successfully!')
                update_session_auth_hash(request,form.user)
                return redirect('profile')
            else:
                messages.error(request,"Password's you entered didn't match! Try again")
                return redirect('change_password')
        else:
            form = PasswordChangeForm(user=request.user)
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
        cartItems = order.get_cart_item
        categories = Categories.objects.all()
        context = {'form':form,'categories':categories,'cartItems':cartItems}
        return render(request,'store/changepassword.html',context)
    else:
        return redirect('login')

def success_handler(request):
    if request.method == 'POST':
        try:
            data =request.POST
            myid = int(data['id'])
            order=Order.objects.get(id=myid,customer=request.user)
            customer = request.user
            items = order.orderitem_set.all()
            emaildata = {'name':customer.first_name,'customer':customer,'order':order,'items':items}
            template = render_to_string('store/email_template.html',emaildata)
            email = EmailMessage(
                'Thanks for your purchase',
                template,
                settings.EMAIL_HOST_USER,
                [customer.email]
                )
            email.fail_silently = False
            email.send()
            return JsonResponse({'sent':"messege sent"})
        except:
            return JsonResponse({'sent':"messege sent"})
    else:
         return HttpResponse('error')   
    # elif order.complete==True and order.emailconfirm==True:
    #     return render(request,'store/success.html',context)
    
        
def success(request,myid):
    try:
        order=Order.objects.get(id=myid)
    except:
        return HttpResponse('error')
    customer = order.customer
    items = order.orderitem_set.all()
    context = {'customer':customer,'order':order,'items':items}
    if order.complete==True:
        return render(request, 'store/success.html',context)
    else:
        return HttpResponse('error')

def contactUs(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_item':0,'shipping': False}
        cartItems = order['get_cart_item']
    if request.method == 'POST':
        print('hello')
        messages.success(request,'Your response has been regestered successfully!')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        response = request.POST.get('response')
        ContactUs.objects.create(
            firstname=firstname,
            lastname = lastname,
            email = email,
            response = response,
        )
        return redirect('contactus')
    else:
        pass
    categories = Categories.objects.all()
    context= {'categories': categories,'cartItems':cartItems}
    return render(request,'store/contactus.html',context)

def aboutUs(request):
    return render(request,'store/aboutus.html')

def reviews(request,myid):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_item':0,'shipping': False}
        cartItems = order['get_cart_item']
    product = Product.objects.get(id=myid)
    reviews = Reviews.objects.filter(product=product)
    categories = Categories.objects.all()
    context= {'product': product,'reviews':reviews[::-1],'categories': categories,'cartItems':cartItems}
    return render(request,'store/reviews.html',context)


def addmultipleProd(request):
    if request.is_ajax():
        data = request.POST
        productId = data['productId']
        action = data['action']
        print('Action:',action)
        print('ProductId:',productId)
        product = Product.objects.get(id=productId)
        customer = request.user  
        order, created = Order.objects.get_or_create(customer=customer , complete=False)
        orderItem, created = OrderItem.objects.get_or_create(customer=customer,order=order,product=product)
        if action == "add" and (orderItem.quantity<5 and orderItem.quantity<orderItem.product.stock) :
            orderItem.quantity +=1
        elif action == "remove":
            orderItem.quantity-=1
        orderItem.save()
        if orderItem.quantity<=0 or action=="delete":
            orderItem.delete()
        total = order.get_cart_total
        tax = (5*total)/100
        print(tax)
        grandTotal = tax + total
        print(grandTotal)
        return JsonResponse({'msg':"success",'quantity':orderItem.quantity,'total':orderItem.get_total,'orderTotal':total,'grandTotal':grandTotal,'items':order.get_cart_item,'tax':tax})
    return HttpResponse('ERROR PAGE NOT FOUND')


@login_required(login_url='login')
def orderDetails(request,myid):
    customer = request.user
    orders = Order.objects.get(id=myid,customer=customer,complete=True)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_item':0,'shipping': False}
        cartItems = order['get_cart_item']
    item = orders.orderitem_set.all()
    categories = Categories.objects.all()
    context = {'items':items, 'cartItems':cartItems,'categories':categories,'orders':orders,'customer':customer,'item':item}

    return render(request, 'store/orderDetails.html',context)

@login_required(login_url='login')
def update_address(request,myid):
    customer = request.user
    address = ShippingAddress.objects.get(id=myid,customer=customer)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_item':0,'shipping': False}
        cartItems = order['get_cart_item']
    if request.method == "POST":
        mainaddress = AllAddresses.objects.get(customer=customer,mainaddressmodel=address)
        mainaddress.mainaddressmodel=None
        mainaddress.save()
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        addresss = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        phonenumber =request.POST.get('phonenumber')

        address.first_name = first_name
        address.last_name = last_name
        address.address = addresss
        address.city = city
        address.state = state
        address.zipcode = zipcode
        address.phonenumber = phonenumber
        address.save()

        AllAddresses.objects.create(
            customer=customer,
            first_name=first_name,
            last_name=last_name,
            address=addresss,
            city=city,
            state=state,
            zipcode=zipcode,
            phonenumber=phonenumber,
            mainaddressmodel=address
        )
        return redirect('checkout')
    
    categories = Categories.objects.all()
    context = {'items':items, 'cartItems':cartItems,'categories':categories,'customer':customer,'address':address}

    return render(request, 'store/update_address.html',context)
@csrf_exempt
def handlerequest(request):
    # post request by paytm
    if request.method == 'POST':
        try:
            form = request.POST
            response_dict = {}
            for i in form.keys():
                response_dict[i] = form[i]
                if i == "CHECKSUMHASH":
                    check_sum = form[i]
            verify = checksum.verify_checksum(param_dict=response_dict,merchant_key= "ke3Q@9&y8857%kZ&",checksum=check_sum)
            order = Order.objects.get(id=request.POST.get('ORDERID'), complete=False)
            customer = order.customer
            if verify:
                if response_dict['RESPCODE'] == '01':
                    print(request.POST)
                    order.transaction_id = request.POST.get('TXNID')
                    tax = (5*order.get_cart_total)/100
                    grandTotal = tax + order.get_cart_total
                    order.total = order.get_cart_total
                    order.tax = tax
                    order.grandtotal = grandTotal
                    order.complete = True
                    order.status = 'Order Processing'
                    order.save()
                    items = order.orderitem_set.all()
                    for item in items:
                        prod = Product.objects.get(id=item.product.id)
                        item.sp = item.get_total
                        item.save()
                        prod.stock -= item.quantity
                        if prod.stock<=0:
                            prod.available = False
                        prod.save()  
                    context = {'customer':customer,'order':order,'items':items}
                    emaildata = {'name':customer.first_name,'customer':customer,'order':order,'items':items}
                    try:
                        template = render_to_string('store/email_template.html',emaildata)
                        email = EmailMessage(
                            'Thanks for your purchase',
                            template,
                            settings.EMAIL_HOST_USER,
                            [customer.email]
                        )
                        email.fail_silently = False
                        email.send()
                    except:
                        pass
                    return render(request, 'store/success.html',context)
                else:
                    items = order.orderitem_set.all()
                    new_order, created = Order.objects.get_or_create(customer=customer, complete=False,transaction_id=datetime.datetime.now().timestamp())
                    for item in items:
                        item.order=new_order
                        item.save()
                    new_order.transaction_id = ""
                    new_order.save()
                    order.delete()
                    messages.error(request,response_dict['RESPMSG'])
                    return redirect('checkout') 
            else:
                items = order.orderitem_set.all()
                new_order, created = Order.objects.get_or_create(customer=customer, complete=False,transaction_id=datetime.datetime.now().timestamp())
                for item in items:
                    item.order=new_order
                    item.save()
                new_order.transaction_id = ""
                new_order.save()
                order.delete()
                messages.error(request,response_dict['RESPMSG'])
                return redirect('checkout')
            # if order.shipping == True:
            #     shippingaddress=ShippingAddress.objects.get(id=int(request.session['address_id']))
            #     address = AllAddresses.objects.get(mainaddressmodel=shippingaddress)
            #     order.address = address
            #     order.date_orderd = datetime.date.today()
            # order.save()   
        except:
            return HttpResponse('ERROR1')
    else:
        return HttpResponse('ERROR2')






#DELETING A SESSION
def del_session(request):
    if request.is_ajax():
        try:
            del request.session['prod_id']
            del request.session['custom_url']
            return JsonResponse({'msg':'done'})
        except KeyError:
            pass
    return HttpResponse("ERROR PAGE")


