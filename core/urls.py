from django.urls import path
from .views import(
										ProductListView, 
										ProductDetailView, 
										add_to_cart, remove_from_cart, 
										CartListView,
										remove_single_item_from_cart,
										CheckoutView,
										PaymentView,
										StripeIntentView,
										ReviewView
                  )

urlpatterns = [
	path('', ProductListView.as_view(), name='product_list_view'),
	path('products/<slug>', ReviewView.as_view(), name='product_detail_view'),
	path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
	path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
	path('cart/', CartListView.as_view(), name='cart-list'),
	path('remove-single-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
	path('checkout/', CheckoutView.as_view(), name='checkout'),
	path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
	path('payment/stripe/create-payment-intent/', StripeIntentView.as_view(), name='create-payment-intent')
]