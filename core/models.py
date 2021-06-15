from django.db import models
from django.shortcuts import redirect, reverse
from django.conf import settings
from django_countries.fields import CountryField

class Item(models.Model):
  title = models.CharField(max_length=100)
  price = models.FloatField()
  stock = models.IntegerField()
  description = models.TextField(null=True)
  image = models.ImageField(default='default.png', upload_to='product_pics')
  slug  = models.SlugField()

  def __str__(self):
    return str(self.title)
    
  def get_absolute_url(self):
    return reverse('product_detail_view', kwargs={
      'slug': self.slug
    })

  def get_add_to_cart_url(self):
    return reverse('add-to-cart', kwargs={
      'slug': self.slug
    })

  def get_remove_from_cart_url(self):
    return reverse('remove-from-cart', kwargs={
      'slug': self.slug
    })

class OrderItem(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  quantity = models.IntegerField(default=1)
  ordered = models.BooleanField(default=False)

  def __str__(self):
    return str(self.item.title)

  def get_amount(self):
    return self.quantity*self.item.price

  

class Order(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
  item = models.ManyToManyField(OrderItem)
  start_date = models.DateTimeField(auto_now_add=True)
  ordered_date = models.DateTimeField()
  ordered = models.BooleanField(default=False)
  billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, null=True )

  def __str__(self):
    return str(self.user.email)

  def get_final_amount(self):
    total = 0
    for order in self.item.all():
      total += order.get_amount()
    
    return total
    
class BillingAddress(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
  address1 = models.CharField(max_length=100)
  address2 = models.CharField(max_length=100)
  country = CountryField(multiple=False)
  zip_code = models.CharField(max_length=100)

  def __str__(self):
    return self.user.email

class Review(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
  item = models.ForeignKey(Item, 
                            on_delete=models.CASCADE,
                            related_name='reviews')
  review = models.TextField()
  date_added = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return str(self.user.email)
