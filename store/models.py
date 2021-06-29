from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import timezone
from django.db.models.fields import EmailField
# Create your models here
class Manager(BaseUserManager):
    def create_user(self, email, password =None):
        if not email:
            raise ValueError('User must have an email')
        user = self.model(
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    def create_superuser(self , email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password=password

        )
        user.is_admin = True
        user.is_staff = True
        user.save(using = self._db)
        return user
class User(AbstractBaseUser):
    email               = models.EmailField(verbose_name='Email',max_length=50,unique=True)
    first_name          = models.CharField(verbose_name='first name',max_length=60)
    last_name           = models.CharField(verbose_name='last name',max_length=60)
    date_joined         = models.DateTimeField(default=timezone.now)
    is_admin            = models.BooleanField(default=False)
    is_staff            = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True)


    USERNAME_FIELD      = 'email'

    objects = Manager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    


class Categories(models.Model):
    category = models.CharField(max_length=30, null = True)
    def __str__(self):
        return self.category

class Material(models.Model):
    material = models.CharField(max_length=30, null = True)
    def __str__(self):
        return self.material
    



class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=300,null=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, blank=True, null=True)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    stock = models.IntegerField(default=0,null=True)
    available = models.BooleanField(default=False, null=True, blank=False )
    digital = models.BooleanField(default=False, null=True, blank=False )
    dyeable = models.BooleanField(default=False, null=True, blank=False )
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.name
        
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url= ''
        return url

    @property
    def avg_review(self):
        total=None
        reviews = Reviews.objects.filter(product=self)
        temp = [review.rating for review in reviews]
        if sum(temp):
            total = sum(temp)/len(temp)
        return total

    @staticmethod
    def get_avg_review(product):
        total=None
        reviews = Reviews.objects.filter(product=product)
        temp = [review.rating for review in reviews]
        if sum(temp):
            total = sum(temp)/len(temp)
        return total

    @staticmethod
    def get_product_by_material_id(material_id):
        if material_id:
            return Product.objects.filter(material = material_id)
        else:
            return Product.objects.all()
    @staticmethod
    def get_product_if_dyeable(dyeable_bool):
        if dyeable_bool:
            return Product.objects.filter(dyeable = dyeable_bool)
        else:
            return Product.objects.all()



class Images(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.title
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
        


   

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    phonenumber = models.CharField(max_length=13,default=0,null=True,blank=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateField(auto_now_add=True)
    def __str__(self):
        return str(self.pk)

class Reviews(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    comment = models.TextField()
    date_added = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0,validators=[MaxValueValidator(5),MinValueValidator(0),])

    def __str__(self):
        return str(self.pk)

class AllAddresses(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    phonenumber = models.CharField(max_length=13,default=0,null=True,blank=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateField(auto_now_add=True)
    mainaddressmodel = models.ForeignKey(ShippingAddress,on_delete=models.SET_NULL,blank=True,null=True)
    def __str__(self):
        return str(self.pk)

class Order(models.Model):
    STATUS=(('Order Processing','Order Processing'),
            ('In transit','In transit'),
            ('Order Completed','Order Completed'))
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_orderd =  models.DateField(auto_now_add=True)
    status = models.CharField(max_length=200,null=True, choices=STATUS)
    complete = models.BooleanField(default=False, null=True, blank=False)
    total = models.DecimalField(max_digits=7,decimal_places=2,default=0)
    tax = models.DecimalField(max_digits=7,decimal_places=2,default=0)
    grandtotal = models.DecimalField(max_digits=7,decimal_places=2,default=0)
    transaction_id = models.CharField(max_length=200, null=True)
    address = models.ForeignKey(AllAddresses,on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    @property
    def get_cart_item(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    sp = models.DecimalField(max_digits=7,decimal_places=2,default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ContactUs(models.Model):
    firstname = models.CharField(max_length=40, null=True)
    lastname = models.CharField(max_length=40, null=True)
    email = models.EmailField(null=True,max_length=200)
    response = models.TextField(max_length=400,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.email)