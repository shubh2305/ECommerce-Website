from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from .models import Item, OrderItem, Order, BillingAddress, Review
from .forms import CheckoutForm, ReviewForm

import stripe
from stripe.api_resources import review

stripe.api_key=settings.STRIPE_SECRET_KEY

class ProductListView(ListView):
  model = Item
  template_name = 'core/home.html'
  context_object_name = 'products'
    

class ProductDetailView(LoginRequiredMixin, DetailView):
  model = Item
  template_name = 'core/item_detail.html'
  context_object_name = 'product'

class CartListView(View):
  def get(self, *args, **kwargs):
    try:
      orders = Order.objects.get(user=self.request.user, ordered=False)
    except:
      return render(self.request, 'core/cart_list_view.html')
    return render(self.request, 'core/cart_list_view.html', {'orders':orders})

class CheckoutView(View):
  def get(self, *args, **kwargs):
    form = CheckoutForm()
    context = {
      'form': form
    }
    return render(self.request, 'core/checkout.html', context=context)

  def post(self, *args, **kwargs):
    form = CheckoutForm(self.request.POST or None)
    try:
      order = Order.objects.get(user=self.request.user, ordered=False)
      if form.is_valid():
        address1 = form.cleaned_data['address1']
        address2 = form.cleaned_data['address2']
        country = form.cleaned_data['country']
        zip_code = form.cleaned_data['zip_code']
        billing_address = BillingAddress(
          user = self.request.user,
          address1 = address1,
          address2 = address2,
          country = country,
          zip_code = zip_code,
        )
        billing_address.save()
        order.billing_address = billing_address
        order.save()

      return redirect('payment', payment_option='stripe')
    except ObjectDoesNotExist:
      return redirect('cart-list')

class ReviewView(View):
  def get(self, *args, **kwargs):
    product = Item.objects.get(slug=kwargs['slug'])
    form = ReviewForm()
    context = {
      'form' : form,
      'product':product
    }
    return render(self.request, 'core/item_detail.html', context=context)

  def post(self, *args, **kwargs):
    form = ReviewForm(self.request.POST or None)
    if form.is_valid():
      review = form.cleaned_data['review']
      review_model_object = Review(
        user=self.request.user,
        item=Item.objects.get(slug=kwargs['slug']),
        review=review
      )
      review_model_object.save()

    return redirect('product_detail_view', slug=kwargs['slug'])

class PaymentView(View):
  def get(self, *args, **kwargs):
    orders = Order.objects.get(user=self.request.user, ordered=False)
    return render(self.request, 'core/payment.html', {'orders':orders})

  def post(self, *args, **kwargs):
    print(self.request.POST)
    intent = stripe.PaymentIntent.create(
      amount=1099,
      currency='usd',
    )
    return redirect('payment', payment_option='stripe')

def add_to_cart(request, slug):
  item = get_object_or_404(Item, slug=slug)
  order_item, created = OrderItem.objects.get_or_create(
      item=item,
      user=request.user,
      ordered=False
    )
  order_query_set = Order.objects.filter(
      user=request.user, 
      ordered=False
    )
  if len(order_query_set):
    order = order_query_set[0]
    if order.item.filter(item__slug=item.slug).exists():
      order_item.quantity += 1
      order_item.save()
    else:
      order_item.quantity = 1
      order_item.save()
      order.item.add(order_item)
  else:
    order = Order.objects.create(user=request.user, ordered_date=timezone.now())
    order.item.add(order_item)

  return redirect('cart-list')

def remove_from_cart(request, slug):
  item = get_object_or_404(Item, slug=slug)

  order_query_set = Order.objects.filter(
    user=request.user,
    ordered=False
  )

  if len(order_query_set):
    order = order_query_set[0]
    if order.item.filter(item__slug=item.slug).exists():
      order_item = OrderItem.objects.filter(
          item=item,
          user=request.user,
          ordered=False
        )[0]
      order_item.quantity = 0
      order_item.save()
      order.item.remove(order_item)
    else: 
      return redirect('cart-list')

  return redirect('cart-list')

def remove_single_item_from_cart(request, slug):
  item = get_object_or_404(Item, slug=slug)

  order_query_set = Order.objects.filter(
    user=request.user,
    ordered=False
  )

  if len(order_query_set):
    order = order_query_set[0]
    if order.item.filter(item__slug=item.slug).exists():
      order_item = OrderItem.objects.filter(
          item=item,
          user=request.user,
          ordered=False
        )[0]
      if order_item.quantity <= 1:

        order.item.remove(order_item)
      else:
        order_item.quantity -= 1
        order_item.save()
    else: 
      return redirect('cart-list')

  return redirect('cart-list')

class StripeIntentView(View):
  def post(self, *args, **kwargs):
    try:
      orders = Order.objects.get(user=self.request.user, ordered=False)
      intent = stripe.PaymentIntent.create(
          amount=200,
          currency='usd'
      )
      print(intent)
      print(intent['client_secret'])
      return JsonResponse({
        'clientSecret': intent['client_secret']
      })
    except Exception as e:
      return JsonResponse({'error':str(e)})