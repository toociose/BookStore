from django.db import models
from django.contrib.auth.models import User
class Users(models.Model):
    fname= models.CharField(max_length=100,null=True)
    lname= models.CharField(max_length=100,null=True)
    email= models.EmailField(max_length=254,null=True)
    phone= models.CharField(max_length=100,null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,null = True)
    status = models.BooleanField(default=True)
    promotion = models.BooleanField(default=False)
    def get_fname(self):
        return self.fname

class Address(models.Model):
    users = models.ForeignKey(Users, on_delete=models.CASCADE)
    street = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=100, null=True)

class CreditCard(models.Model):
    users = models.ForeignKey(Users, on_delete=models.CASCADE)
    cardnumber = models.CharField(max_length=100, null=True)
    day = models.CharField(max_length=20, null=True)
    year = models.CharField(max_length=20, null=True)
    cvc = models.CharField(max_length=20, null=True)

class Usertypes(models.Model):
    usertypeid = models.IntegerField(db_column='UserTypeID', primary_key=True)  # Field name made lowercase.
    usertypename = models.CharField(db_column='UserTypeName', max_length=45, blank=True, null=True)  # Field name made lowercase.


class Book(models.Model):
    bookid = models.IntegerField(db_column='BookID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=45, blank=True, null=True)  # Field name made lowercase.
    isbn = models.CharField(db_column='ISBN', max_length=45, blank=True, null=True)  # Field name made lowercase.
    author = models.CharField(db_column='Author', max_length=45, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=45, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(max_length=1000, blank=True, null=True)
    cover_picture = models.CharField(db_column='Cover picture', max_length=45, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    year = models.CharField(db_column='Year', max_length=45, blank=True, null=True)  # Field name made lowercase.
    link = models.CharField(max_length=45, blank=True, null=True)
    img = models.CharField(max_length=45, blank=True, null=True)
    price = models.FloatField(blank=True, null=True, default=True) 

class Carts(models.Model):
    userid = models.ForeignKey(Users, models.DO_NOTHING, db_column='UserID', blank=True, null=True)  # Field name made lowercase.

class CartItem(models.Model):
    cartid = models.ForeignKey(Carts, models.DO_NOTHING, db_column='CartsId')  # Field name made lowercase.
    bookid = models.ForeignKey(Book, models.DO_NOTHING, db_column='bookID', blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField(max_length=20, db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    orderstatus = models.BooleanField(default=False)

class Total(models.Model):
    price = models.FloatField(blank=True, null=True, default=True)
    cartid = models.ForeignKey(Carts, models.DO_NOTHING, db_column='CartsId')  # Field name made lowercase.
    promoApplied = models.BooleanField(default=False)
    promoCode = models.CharField(db_column='PromoCode', max_length=10, blank=True, null=True, default = False)

class Inventbookid(models.Model):
    idinventbookid = models.IntegerField(db_column='idInventBookID', primary_key=True)  # Field name made lowercase.
    bookidfk = models.ForeignKey(Book, models.DO_NOTHING, db_column='BookIdFK', blank=True, null=True)  # Field name made lowercase.
    quantityonhand = models.IntegerField(db_column='QuantityOnHand', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(max_length=45, blank=True, null=True)
    price = models.CharField(max_length=45, blank=True, null=True)


class Order(models.Model):
    orderid = models.IntegerField(db_column='orderID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userID', blank=True, null=True)  # Field name made lowercase.
    cardid = models.ForeignKey('CreditCard', models.DO_NOTHING, db_column='cardID', blank=True, null=True)  # Field name made lowercase.
    grandtotal = models.CharField(db_column='grandTotal', max_length=45, blank=True, null=True)  # Field name made lowercase.
    promoid = models.ForeignKey('Promotion', models.DO_NOTHING, db_column='promoID', blank=True, null=True)  # Field name made lowercase.
    orderdatetime = models.CharField(db_column='orderDateTime', max_length=45, blank=True, null=True)  # Field name made lowercase.

class Orders(models.Model):
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userID', blank=True, null=True)  # Field name made lowercase.
    cardid = models.ForeignKey('CreditCard', models.DO_NOTHING, db_column='cardID', blank=True, null=True)  # Field name made lowercase.
    grandtotal = models.CharField(db_column='grandTotal', max_length=45, blank=True, null=True)  # Field name made lowercase.
    orderdatetime = models.CharField(db_column='orderDateTime', max_length=45, blank=True, null=True)  # Field name made lowercase.


class Transactions(models.Model):
    orderid = models.ForeignKey(Orders, models.DO_NOTHING, db_column='orderID', blank=True, null=True)  # Field name made lowercase.
    bookid = models.ForeignKey(Book, models.DO_NOTHING, db_column='bookID', blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField(blank=True, null=True)
class Promotion(models.Model):
    promoid = models.IntegerField(db_column='PromoID', primary_key=True)  # Field name made lowercase.
    startdate = models.CharField(db_column='StartDate', max_length=45, blank=True, null=True)  # Field name made lowercase.
    enddate = models.CharField(db_column='EndDate', max_length=45, blank=True, null=True)  # Field name made lowercase.
    discount = models.CharField(db_column='Discount', max_length=45, blank=True, null=True)  # Field name made lowercase.
    promoCode = models.CharField(db_column='PromoCode', max_length=10, blank=True, null=True)