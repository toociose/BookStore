from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Users, Address, CreditCard,Book,CartItem,Carts,Promotion, Orders,Total,Transactions
import datetime
# Create your views here.
def indexView(request):
    allbooks= Book.objects.all()
    promos = Promotion.objects.all()
    infos = Users.objects.all()
    return render(request, 'index.html',{'allbooks':allbooks, 'promos':promos, 'infos':infos})

def dashboardView(request):
    return render(request, 'dashboard.html')

@login_required
def remove_from_cart(request, **kwargs):
    user = Users.objects.get(email = request.user.email)
    cart = Carts.objects.get(userid = user)
    book = Book.objects.filter(title=kwargs.get('item_id',"")).first()
    totals = Total.objects.get(cartid= cart)
    if totals.promoApplied is True:
        totalPrice = Total.objects.get(cartid = cart)
        Promo = totalPrice.promoCode
        promotion = Promotion.objects.get(promoCode = Promo)
        priceOff = int(promotion.discount)
        discountPrice = book.price * (priceOff/100)
        totalPrice.price = totalPrice.price - book.price + discountPrice
        totalPrice.price = round(totalPrice.price, 2)
        totalPrice.save(update_fields=['price'])
    else:
        totals.price = totals.price - book.price
        totals.price = round(totals.price, 2)
        totals.save(update_fields=['price'])
    
    if totals.price < 0:
        totals.price = 0
        totals.save(update_fields=['price'])
        totals.promoApplied = False
        totals.save(update_fields=['promoApplied'])
        totals.promoCode = "False"
        totals.save(update_fields=['promoCode'])
    remove = CartItem.objects.get(bookid =book,cartid =cart)
    remove.delete()
  
    return redirect('checkout_url')


def checkoutView(request):
    infos = Users.objects.all()
    addys = Address.objects.all()
    creditscards = CreditCard.objects.all()
    cartitems = CartItem.objects.all()
    carts = Carts.objects.all()
    books = Book.objects.all()
    totals = Total.objects.all()
    if request.POST:
        if 'checkout' in request.POST:
            cardnumber = request.POST['credit-numbers']
            creditcard = CreditCard.objects.get(cardnumber =cardnumber)
            currentUser = Users.objects.get(email =request.user.email)
            cart = Carts.objects.get(userid = currentUser)
            total = Total.objects.get(cartid = cart)
            date = datetime.date.today()
            order = Orders(userid= currentUser, cardid= creditcard, grandtotal=total.price, orderdatetime=date)
            order.save()
            for cartitem in cartitems:
                if cartitem.cartid == cart:
                    for book in books:
                        if cartitem.bookid == book:
                            items = CartItem.objects.get(cartid=cart, bookid=book)
                            transactions = Transactions(bookid= book, quantity = 1, orderid = order)
                            transactions.save()
                            items.delete()
                            total.price = 0
                            total.save(update_fields=['price'])


            return redirect('ordercomplete_url')
        elif 'addAddy' in request.POST:
            street= request.POST['street']
            city = request.POST['city']
            state = request.POST['state']
            zipcode = request.POST['zip']
            user = Users.objects.get(email=request.user.email)
            userAddress = Address.objects.get(users=user)
            userAddress.street=street
            userAddress.city=city
            userAddress.state=state
            userAddress.zipcode=zipcode
            userAddress.save()
            return redirect('checkout_url')
        elif 'applyPromo' in request.POST:
            print('hello')
            Promo = request.POST['promo']
            user = Users.objects.get(email=request.user.email)
            cart = Carts.objects.get(userid = user)
            promotion = Promotion.objects.get(promoCode = Promo)
            totalPrice = Total.objects.get(cartid = cart)
            totalPrice.promoApplied = True
            totalPrice.save(update_fields=['promoApplied'])
            totalPrice.promoCode = Promo
            totalPrice.save(update_fields=['promoCode'])
            priceOff = int(promotion.discount)
            discountPrice = totalPrice.price * (priceOff/100)
            totalPrice.price = totalPrice.price - discountPrice
            totalPrice.price = round(totalPrice.price, 2)
            totalPrice.save(update_fields=['price'])
            return redirect('checkout_url')
        elif 'addCard' in request.POST:
            cardnumber = request.POST['cardnumber']
            day = request.POST['day']
            year =request.POST['year']
            cvc = request.POST['cvc']
            user = Users.objects.get(email=request.user.email)
            userCredit = CreditCard(users = user, cardnumber = cardnumber, day = day, year=year, cvc=cvc)
            userCredit.save()
            return redirect('checkout_url')
    else:
        return render(request, 'checkout.html', {'infos':infos,'addys':addys,'creditscards':creditscards,'cartitems':cartitems,'carts':carts,'books':books, 'totals':totals})

def ordercompleteView(request):
    peoples = Users.objects.all()
    orders = Orders.objects.all()
    return render(request, 'ordercomplete.html', {'peoples':peoples,'orders':orders})

def logoutView(request):
    auth.logout(request)
    print('worded')
    return redirect('home')

def adminView(request):
    return redirect('admin')

def historypageView(request):
    allbooks= Book.objects.all()
    return render(request, 'historypage.html',{'allbooks':allbooks})

def romancepageView(request):
    allbooks= Book.objects.all()
    return render(request, 'romancepage.html',{'allbooks':allbooks})


def mysterypageView(request):
    allbooks= Book.objects.all()
    return render(request, 'mysterypage.html',{'allbooks':allbooks})

    
def fantasypageView(request):
    allbooks= Book.objects.all()
    return render(request, 'fantasypage.html',{'allbooks':allbooks})

def profileView(request):
    infos = Users.objects.all()
    addys = Address.objects.all()
    creditscards = CreditCard.objects.all()
    if request.POST:
        if 'remove' in request.POST:
            cardnumber = request.POST['credit-numbers']
            remove = CreditCard.objects.get(cardnumber =cardnumber)
            remove.delete()
            return redirect('profile_url')
        elif 'subscribe' in request.POST:
            promotion = request.POST['True']
            user = Users.objects.get(email = request.user.email)
            user.promotion = promotion
            user.save(update_fields=['promotion'])
            return redirect('profile_url')
        elif 'unsubscribe' in request.POST:
            promotion = request.POST['False']
            user = Users.objects.get(email = request.user.email)
            user.promotion = promotion
            user.save(update_fields=['promotion'])
            return redirect('profile_url')
        elif 'changeF' in request.POST:
            fname = request.POST['fname3']
            user = Users.objects.get(email = request.user.email)
            user2 = User.objects.get(email= request.user.email)
            user.fname = fname
            user.save(update_fields=['fname'])
            user2.first_name = fname
            user2.save(update_fields=['first_name'])
            return redirect('profile_url')
        elif 'changeL' in request.POST:
            lname = request.POST['lname3']
            user = Users.objects.get(email = request.user.email)
            user2 = User.objects.get(email= request.user.email)
            user.lname = lname
            user.save(update_fields=['lname'])
            user2.last_name = lname
            user2.save(update_fields=['last_name'])
            return redirect('profile_url')
        elif 'changeP' in request.POST:
            phone = request.POST['phone2']
            user = Users.objects.get(email = request.user.email)
            user.phone = phone
            user.save(update_fields=['phone'])
            return redirect('profile_url')
        elif 'addAddy' in request.POST:
            street= request.POST['street']
            city = request.POST['city']
            state = request.POST['state']
            zipcode = request.POST['zip']
            user = Users.objects.get(email=request.user.email)
            userAddress = Address.objects.get(users=user)
            userAddress.street=street
            userAddress.city=city
            userAddress.state=state
            userAddress.zipcode=zipcode
            userAddress.save()
            return redirect('profile_url')
        elif 'addCard' in request.POST:
            cardnumber = request.POST['cardnumber']
            day = request.POST['day']
            year =request.POST['year']
            cvc = request.POST['cvc']
          
            user = Users.objects.get(email=request.user.email)
            userCredit = CreditCard(users = user, cardnumber = cardnumber, day = day, year=year, cvc=cvc)
            userCredit.save()
            return redirect('profile_url')
    else:
        return render(request, 'profile.html', {'infos':infos, 'addys':addys, 'creditscards':creditscards})

def bookpageView(request):
    allbooks= Book.objects.all()
    return render(request, 'bookpage.html',{'allbooks':allbooks})
@login_required
def add_to_cart(request, **kwargs):
    user = Users.objects.get(email = request.user.email)
    #user = Users.objects.get(fname = request.user.first_name)
    cart = Carts.objects.get(userid = user)
    book = Book.objects.filter(title=kwargs.get('item_id',"")).first()
    cartitem = CartItem(bookid =book, cartid = cart, quantity =1, orderstatus=False)
    cartitem.save()
    totals = Total.objects.get(cartid= cart)
    if totals.promoApplied is True:
        totalPrice = Total.objects.get(cartid = cart)
        if totalPrice.promoCode != "False":
            Promo = totalPrice.promoCode
            promotion = Promotion.objects.get(promoCode = Promo)
            priceOff = int(promotion.discount)
            discountPrice = book.price * (priceOff/100)
            totalPrice.price = totalPrice.price + book.price - discountPrice
            totalPrice.price = round(totalPrice.price, 2)
            totalPrice.save(update_fields=['price'])
    else:
        totals.price = totals.price + book.price
        totals.price = round(totals.price, 2)
        totals.save(update_fields=['price'])
    return redirect('bookpage_url')

def go_to_page(request, **kwargs):
    book = Book.objects.filter(title=kwargs.get('item_id',"")).first()
   
    return render(request, 'firstbook.html',{'book':book})

def firstbookView(request):
  return render(request, 'firstbook.html')

def loginView(request):
    if request.method == 'POST':
        username = request.POST['account']
        password = request.POST['userpass']

        user = auth.authenticate(username=username, password=password)
        emailuser=None
        try:
            emailuser = User.objects.get(email=username) 
            pass
        except Exception:
            pass

        if emailuser != None:
            email_valid = emailuser.check_password(password) 

        if user is not None:
            if username == 'Bum':
                return redirect('admin')
            else: 
                auth.login(request,user)
                print('worked')
                return redirect('home')
        elif email_valid:
            auth.login(request,emailuser)
            print('worked')
            return redirect('home')
        else:
            print('passwords do not match match')
            messages.info(request,'invalid credentials')
            return redirect('login_url')
    else:
        return render(request,'registration/login.html')

def registerView(request):
    if request.method == "POST":
        username = request.POST['fname']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        password1 = request.POST['password']
        password2 = request.POST['repassword']
        promotion = request.POST.get('True')

        street= request.POST['street']
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zip']

        cardnumber = request.POST['cardnumber']
        day = request.POST['day']
        year =request.POST['year']
        cvc = request.POST['cvc']

        if User.objects.filter(email=email).exists():
            print('email already is in use')
            return render(request, 'registration/register.html')
        elif password1 == password2:
            userInfo = Users(fname=first_name,lname=last_name,email = email,phone=phone)
            userInfo.save()
            userAddress = Address(users = userInfo, street=street, city =city, state=state, zipcode = zipcode)
            userAddress.save()
            userCredit = CreditCard(users = userInfo, cardnumber = cardnumber, day = day, year=year, cvc=cvc)
            userCredit.save()
            user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
            user.save()
            userCart = Carts(userid= userInfo)
            userCart.save()
            totalprice =Total(price= 0, cartid= userCart)
            totalprice.save()
            if promotion == True:
                userInfo.promotion = promotion
                userInfo.save(update_fields=['promotion'])
                print('worked')
                return redirect('dashboard_url')
            else:
                print('worked')
                return redirect('dashboard_url')
        else:
            print('passwords do not match match')
            return render(request, 'registration/register.html')
    else:
        return render(request, 'registration/register.html')

def orderhistoryView(request):
  # if request.POST:
  listofOrders = Orders.objects.all()
  tranzactions = Transactions.objects.all()
  listofBooks = Book.objects.all()
  listofUsers = User.objects.all()
  addie = Address.objects.all()
  
  if request.method == "POST":
      print("hello")

      if 'Reorder' in request.POST:
            print(request.POST['prodId'])
            print( request.POST['order.id'])
  else:      
    return render(request, 'orderhistory.html', {'listofOrders':listofOrders, 'tranzactions':tranzactions, 
    'listofBooks':listofBooks, 'listofUsers':listofUsers, 'addie':addie})