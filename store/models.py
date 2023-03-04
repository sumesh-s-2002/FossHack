from email.policy import default
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)
    profile_pic = models.ImageField(default="download.jpg")

    def __str__(self):
        return str(self.user)

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)
    product_image = models.ImageField(default="download.jpg")
    #product image

    def __str__(self):
        return self.title

class ProductImages(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, null=True, blank=True)
    image0 = models.ImageField(default="empty.png")
    image1 = models.ImageField(default="empty.png")
    image2 = models.ImageField(default="empty.png")
    image3 = models.ImageField(default="empty.png")

    def __str__(self):
        return str(self.product)

class Collection(models.Model):
    title = models.CharField(max_length=200)
    product = models.ManyToManyField(Product)

    def __str__(self):
        return self.title

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE)

    @property
    def grandTotal(self):
        sum = 0
        for item in self.cartitem_set.all():
            sum += item.total
        return sum

    def __str__(self):
        return str(self.customer)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)

    @property
    def total(self):
        return (self.quantity)*(self.product.price)

    def __str__(self):
        return str(self.product)

class Order(models.Model):
    order_status_choices = [
        ("PENDING","P",), 
        ("SHIPPED","S"),
        ("OUT FOR DELEVERY","O"),
        ("CANCELLED","C"),
        ("DELEVERED","D")
    ]
    
    payment_status_choices = [
        ("P", "PENDING"),
        ("S", "SUCCES"),
        ("F", "FAILED")
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=200,blank=True, null=True)
    order_status = models.CharField(max_length=20, choices=order_status_choices, default="PENDING")
    payment_status = models.CharField(max_length=20, choices=payment_status_choices, default="PENDING")
    address = models.ForeignKey('Address', on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    razorpay_order_id = models.CharField(max_length=500)
    razorpay_payment_id = models.CharField(max_length=500)
    razorpay_signature = models.CharField(max_length=500)


    def __str__(self):
        return str(self.customer)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    unit_price = models.DecimalField(max_digits=9, decimal_places=2)

    @property
    def total(self):
        return self.quantity * self.unit_price
    def __str__(self):
        return str(self.product)

class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip = models.CharField(max_length=10)

    def __str__(self):
        return self.address

class Tag(models.Model):
    tag = models.CharField(max_length=20)
    product = models.ManyToManyField(Product)

