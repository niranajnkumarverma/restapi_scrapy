from django.db import models

# Create your models here.
class User(models.Model):
    FullName = models.CharField(max_length=50)
    Email = models.EmailField(max_length=50, unique=True)
    Mobile = models.CharField(max_length=10)
    Address = models.TextField(max_length=100)
    Password = models.CharField(max_length=12)
    IsActive = models.BooleanField(default=False)
    IsSeller = models.BooleanField(default=False)

    def __str__(self):
        return self.FullName

class Product(models.Model):
    product_seller = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_author = models.CharField(max_length=100)
    product_author = models.CharField(max_length=100)
    product_price = models.IntegerField()
    product_desc = models.TextField()
    product_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.product_name

class WishList(models.Model):
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	date=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.product.product_name+" - "+self.user.FullName

class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    qty=models.CharField(max_length=10, default="1")
    price = models.CharField(max_length=10, default="0")
    total = models.CharField(max_length=10, default="0")

    def save(self, *args, **kwargs):
        if self.price and self.qty:
            self.total = int(self.price) * int(self.qty)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.FullName} - {self.product.product_name} -- {self.product.product_price}"

class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions',on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)